from datetime import datetime
from redis import Redis

REQUEST_LIMIT_PER_MINUTE = 20

redis_conn = Redis(host='localhost', port=6379, db=0)
user_id = 'some_user_id'

for i in range(25):
    # Создадим Pipeline (https://redis.io/topics/pipelining),
    # который позволит отправить несколько команд за один сетевой вызов
    # и добиться атомарности алгоритма
    pipe = redis_conn.pipeline()
    now = datetime.now()
    # Создадим ключ, состоящий из идентификатора пользователя и текущей минуты
    # В итоге будут созданы ключи some_user_id:2, some_user_id:3 и т.д.
    # Так будем считать количество обращений за текущую минуту
    key = f'{user_id}:{now.minute}'
    # Добавим команду в pipeline для увеличения количества
    # обращений пользователя к серверу
    pipe.incr(key, 1)
    # Поставим время жизни ключа — 1 минуту. Это гарантирует, что ключ удалится,
    # и мы сможем начать отсчёт обращений с 0 для этой минуты
    pipe.expire(key, 59)
    # Отправим команды в Redis на исполнение
    result = pipe.execute()
    # Результат работы пайплайна приходит в виде списка
    # Результаты возвращаются в порядке выполнения команд
    # Вам нужно получить результат команды incr, который вернёт информацию,
    # какое по счёту обращение совершил пользователь
    # Так как команда выполнялась первой, то результат будет по нулевому индексу
    request_number = result[0]
    if request_number > REQUEST_LIMIT_PER_MINUTE:
        print('429 Too Many Requests')
    else:
        print('Можно обработать запрос')
