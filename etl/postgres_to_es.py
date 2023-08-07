import os
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from functools import wraps
from time import sleep
from pathlib import Path

FLAG_FILE_PATH = 'sqlite_to_es_active.flag'


def create_loading_flag():
    f = Path(FLAG_FILE_PATH)
    f.touch(exist_ok=True)


def delete_loading_flag():
    os.remove(FLAG_FILE_PATH)


def is_loading_flag_exist() -> bool:
    return os.path.exists(FLAG_FILE_PATH)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое
    время, если возникла ошибка. Использует экспоненциальный
    рост времени повтора (factor) до граничного времени ожидания
    (border_sleep_time)

    Формула:
    t = start_sleep_time * 2^(n) if t < border_sleep_time
    t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time + factor
            if sleep_time < border_sleep_time:
                sleep(sleep_time)
            else:
                sleep(border_sleep_time)
        return inner
    return func_wrapper
