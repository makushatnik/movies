import os
import json
import logging
import requests
import sqlite3
from contextlib import contextmanager
from typing import List
from urllib.parse import urljoin
from pathlib import Path

logger = logging.getLogger("ETL")

ABSENT = 'N/A'
FLAG_FILE_PATH = 'sqlite_to_es_active.flag'


def create_loading_flag():
    f = Path(FLAG_FILE_PATH)
    f.touch(exist_ok=True)


def delete_loading_flag():
    os.remove(FLAG_FILE_PATH)


def is_loading_flag_exist() -> bool:
    return os.path.exists(FLAG_FILE_PATH)


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    yield conn
    conn.close()


class ESLoader:
    def __init__(self, url: str):
        self.url = url

    def _get_es_bulk_query(self, rows: List[dict], index_name: str) -> List[str]:
        """
        Prepares bulk query to ES
        :param rows:        List[dict]
        :param index_name:  str
        :return:            List[str]
        """
        prepared_query = []
        for row in rows:
            prepared_query.extend([
                json.dumps({'index', {'_index': index_name, "_id": row['id']}}),
                json.dumps(row)
            ])
        return prepared_query

    def load_to_es(self, records: List[dict], index_name: str):
        """
        Sending the request to ES & saving data exception handling
        :param records:     List[dict]
        :param index_name:  str
        :return:
        """
        prepared_query = self._get_es_bulk_query(records, index_name)
        str_query = '\n'.join(prepared_query) + '\n'

        headers = {'Content-Type': 'application/x-ndjson'}
        response = requests.post(urljoin(self.url, '_bulk'), data=str_query, headers=headers)
        json_response = json.loads(response.content.decode())
        for item in json_response['items']:
            error_message = item['index'].get('error')
            if error_message:
                logger.error(error_message)


class ETL:
    SQL = '''
     WITH x as (
     -- Используем group_concat, чтобы собрать id и имена
     всех актёров в один список после join'а с таблицей actors
     -- порядок id и имён совпадает
     SELECT m.id, group_concat(a.id) as actors_ids, group_concat(a.name) as
    actors_names
     FROM movies m
     LEFT JOIN movie_actors ma on m.id = ma.movie_id
     LEFT JOIN actors a on ma.actor_id = a.id
     GROUP BY m.id
     )
     -- Получаем список всех фильмов со сценаристами и актёрами
     SELECT m.id, genre, director, title, plot, imdb_rating, x.actors_ids, x.actors_names,
     CASE
     WHEN m.writers = '' THEN '[{"id": "' || m.writer || '"}]'
     ELSE m.writers
     END AS writers
     FROM movies m
     LEFT JOIN x ON m.id = x.id
     '''

    def __init__(self, conn: sqlite3.Connection, es_loader: ESLoader):
        self.conn = conn
        self.es_loader = es_loader

    def load_writers_names(self) -> dict:
        writers = {}
        for writer in self.conn.execute("SELECT DISTINCT id, name FROM writers"):
            writers[writer['id']] = writer
        return writers

    def _transform_row(self, row: dict, writers: dict) -> dict:
        """
        Основная логика преобразования данных из SQLite во внутреннее
        представление ES
        :param row:     dict
        :param writers: dict
        :return:        dict
        """
        movie_writers = []
        writers_set = set()
        for writer in json.loads(row['writers']):
            writer_id = writer['id']
            if writers[writer_id]['name'] != ABSENT and writer_id not in writers_set:
                movie_writers.append(writers[writer_id])
                writers_set.add(writer_id)

        actors = []
        actors_names = []
        if row['actor_ids'] is not None and row['actor_names'] is not None:
            actors = [
                {'id': _id, 'name': name}
                for _id, name in zip(row['actor_ids'].split(','), row['actor_names'].split(','))
                if name != ABSENT
            ]
            actors_names = [x for x in row['actor_names'].split(',') if x != ABSENT]

        return {
            'id': row['id'],
            'genre': row['genre'].replace(' ', '').split(','),
            'writers': movie_writers,
            'actors': actors,
            'actors_names': actors_names,
            'writers_names': [x['name'] for x in movie_writers],
            'imdb_rating': float(row['imdb_rating']) if row['imdb_rating'] != ABSENT else None,
            'title': row['title'],
            'director': [x.strip() for x in row['director'].split(',')] if row['director'] != ABSENT else None,
            'description': row['plot'] if row['plot'] != ABSENT else None
        }

    def load(self, index_name: str):
        """
        Основной метод
        :param index_name: str
        :return:
        """
        if is_loading_flag_exist():
            logger.info('Another loading in process right now!')
            return

        create_loading_flag()

        records = []
        writers = self.load_writers_names()

        for row in self.conn.execute(self.SQL):
            transformed = self._transform_row(row, writers)
            records.append(transformed)

        self.es_loader.load_to_es(records, index_name)
        delete_loading_flag()
