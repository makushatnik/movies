import csv
import json

import requests

CSV_FILE_NAME = "/var/log/super_mega_critical.csv"
SIEM_URL = "http://siem.yandex.ru/input"
FIELDS = []
# TODO Move to DB
STORAGE = []


def load_from_csv():
    global FIELDS
    with open(CSV_FILE_NAME, encoding='utf-8') as r_file:
        fr = csv.reader(r_file, delimiter=",")
        FIELDS = next(fr)
        for row in fr:
            col_num = 0
            new_data = {}
            for col in row:
                new_data[FIELDS[col_num]] = col
                col_num += 1
            STORAGE.append(new_data)


def send_to_siem():
    data = []
    for row in STORAGE:
        new_data = {}
        for field in FIELDS:
            new_data[field] = row[field]
        data.append(new_data)

    headers = {'Content-type': 'application/json'}
    r = requests.post(SIEM_URL, json=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print("Smth went wrong, code=", r.status_code)
    else:
        print("Work was done!")


if __name__ == "__main__":
    load_from_csv()
    send_to_siem()
