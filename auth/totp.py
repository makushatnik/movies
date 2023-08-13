from typing import Dict, Set
from uuid import uuid4
import pyotp
from flask import Flask, redirect, request

app = Flask(__name__)

totp_sync_template = '''
<!DOCTYPE html>
<html>
  <body>
    <canvas id="qr"></canvas>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
    <script>
      (function () {
        var qr = new QRious({
          element: document.getElementById('qr'),
          value: '%s'
        });
      })();
    </script>
    <p>Просканируйте QR-код с помощью TOTP-приложения и введите код</p>
    <form method="post" action="/sync/%s">
      <input required name="code">
      <button type="submit">Синхронизация</button>
    </form>
  </body>
</html>
'''

users_secrets: Dict[str, str] = dict()
verifier_users: Set[str] = set()


@app.route('/')
def sync():
    user_id = str(uuid4())
    # Генерация секретного ключа, на его основе будут создавать коды
    secret = pyotp.random_base32()
    users_secrets[user_id] = secret
    totp = pyotp.TOTP(secret)
    # Ссылка для передачи секретного кода TOTP-приложению. В
    # ссылке можно передать название приложения и имя пользователя
    provisioning_url = totp.provisioning_uri(name=user_id + '@realxaker.ru',
                                             issuer_name='Awesome Cybersecurity app')
    tmpl = totp_sync_template % (provisioning_url, user_id)
    return tmpl


@app.route("/sync/<user_id>", methods=['POST'])
def sync_check(user_id: str):
    # После сканирования QR-кода пользователь отправляет код, сгенерированный в TOTP-приложении
    # Сгенерированный код действителен в течение 30 секунд
    # Достаём из хранилища секретный ключ
    secret = users_secrets[user_id]
    totp = pyotp.TOTP(secret)
    # Верифицируем полученный от пользователя код
    code = request.form['code']
    if not totp.verify(code):
        return 'Неверный код'
    verifier_users.add(user_id)
    return redirect(f'/check/{user_id}')


check_totp_tmpl = '''
<!DOCTYPE html>
<html>
  <body>
    <p>{message}</p>
    <p>Введите код из TOTP-приложения</p>
    <form method="post" action="/check/{user_id}">
      <input required name="code">
       <button type="submit">Синхронизация</button>
    </form>
  </body>
</html>
'''


@app.route("/check/<user_id>")
def render_check_page(user_id: str):
    """
    Запрашиваем код из TOTP-приложения
    :param user_id: str
    :return:
    """
    if user_id not in verifier_users:
        return redirect('/')
    return check_totp_tmpl.format(message='', user_id=user_id)


@app.route("/check/<user_id>", methods=['POST'])
def check(user_id: str):
    """
    Проверяем введенный код
    :param user_id: str
    :return:
    """
    if user_id not in verifier_users:
        return redirect('/')
    code = request.form['code']
    secret = users_secrets[user_id]
    totp = pyotp.TOTP(secret)
    if not totp.verify(code):
        return check_totp_tmpl.format(message='неверный код', user_id=user_id)
    return check_totp_tmpl.format(message='верный код', user_id=user_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
    )
