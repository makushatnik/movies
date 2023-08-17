import os

PROJECT_NAME = os.getenv('PROJECT_NAME', 'notifications')
APP_PORT = os.getenv('APP_PORT', 8000)

RABBIT_HOST = os.getenv('RABBIT_HOST', '127.0.0.1')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5000)

DEFAULT_QUEUE = os.getenv('DEFAULT_QUEUE', 'emails')

SENDER = os.getenv('SENDER', 'login@gmail.com')
PASSWORD = os.getenv('PASSWORD', '')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 465)

ENCODING = 'utf-8'
