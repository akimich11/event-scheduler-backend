from flask import Flask
from sqlalchemy import create_engine
from database.utils import compose_db_url


database_url = compose_db_url()
engine = create_engine(database_url)
app = Flask(__name__)


@app.route('/')
def healthcheck():
    return 'Successful deployment!'


if __name__ == '__main__':
    app.run()
