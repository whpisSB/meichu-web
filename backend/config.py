import os
import dotenv
import pymysql
from datetime import timedelta

dotenv.load_dotenv()

db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")
db_name = os.getenv("MYSQL_DATABASE")

# db_host = 'localhost'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

JWT_SECRET_KEY = '0c3d39b64e91b24ed6df39afdff5ba85c891e38aff5d6ddd669f9e77272b7950'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
JWT_TOKEN_LOCATION = ['headers','query_string']