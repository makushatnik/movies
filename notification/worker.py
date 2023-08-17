import json
import logging
import pika
import smtplib
import sys
from config import *
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue=DEFAULT_QUEUE)


def poll_queue(ch, method, properties, body: bytes):
    # new_notifications = []
    # if new_notifications:
    #     for elem in new_notifications:
    #         send_email(elem.recipient, elem.subject, elem.text)
    if body:
        json_body = json.loads(body.decode(ENCODING))
        print(f" [x] Received {json_body}")


def send_email(recipient: str, subject: str, text: str):
    # server = smtplib.SMTP('localhost', 25)
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER, PASSWORD)

    message = EmailMessage()
    message["From"] = SENDER
    message["To"] = ",".join([recipient])
    message["Subject"] = subject
    message.set_content(text)

    env = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))
    template = env.get_template('templates/mail.html')
    output = template.render(**{
        'title': 'Новое письмо!',
        'text': 'Произошло что-то интересное! :)',
        'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/\
        images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
    })

    message.add_alternative(output, subtype='html')
    server.sendmail(message["From"], [recipient], message.as_string())
    server.close()


def sendmail(recipient: str, msg: str) -> None:
    smtp_port = 587
    smtp_serv = smtplib.SMTP(SMTP_SERVER, smtp_port)
    smtp_serv.ehlo_or_helo_if_needed()
    smtp_serv.starttls()
    smtp_serv.ehlo()
    smtp_serv.login(SENDER, PASSWORD)
    try:
        smtp_serv.sendmail(SENDER, recipient, msg)
    except smtplib.SMTPException:
        logger.exception('cannot send email')
    smtp_serv.quit()


def main():
    channel.basic_consume(queue=DEFAULT_QUEUE, on_message_callback=poll_queue, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        channel.stop_consuming()
        connection.close()
        sys.exit(0)
    except Exception:
        print('Smth went wrong')
        channel.stop_consuming()
        connection.close()
