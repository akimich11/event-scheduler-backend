from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import create_engine

from src.database.db_adapter import DBAdapter
from src.database.models import Base
from src.database.utils import compose_db_url


login_manager = LoginManager()
database_url = compose_db_url()
engine = create_engine(database_url)
db_adapter = DBAdapter(engine)
Base.metadata.create_all(engine)

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE='True'
)
CORS(app, supports_credentials=True, expose_headers=['Set-Cookie'])
app.secret_key = 'acsnlhufeuncoq39840394vjnsdc89493'
login_manager.init_app(app)
