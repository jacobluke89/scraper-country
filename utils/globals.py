import os

from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user = os.environ.get("DB_USER")
pw = os.environ.get("DB_PASSWORD")
db = os.environ.get("DB_NAME")
