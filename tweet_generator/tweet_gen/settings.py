from tornado_sqlalchemy import SQLAlchemy
from alembic.config import Config

config = Config("alembic.ini")
db = SQLAlchemy(config.get_main_option("sqlalchemy.url"))
