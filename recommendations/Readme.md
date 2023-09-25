2 files for Yandex SOC test task:
- load_from_csv.py (task 1)
- Dockerfile (task 2)

Run Docker container every hour:
```
crontab -e
0 * * * * docker run -d loader
```

Task 3:
Возможно, проблема в том, что скрипт запущен из под root'a.