import os

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from .database.db_adapter import DBAdapter
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
CORS(app)
app.config.from_object("src.config.Config")
engine = create_engine(os.getenv('DATABASE_URL'))
db_adapter = DBAdapter(engine)
