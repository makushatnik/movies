from flask import Flask
from db.db import init_db

app = Flask(__name__)


def main():
    init_db(app)
    app.run()


if __name__ == "__main__":
    main()
