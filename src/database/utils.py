import os
from dotenv import load_dotenv


def compose_db_url() -> str:
    load_dotenv()
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
