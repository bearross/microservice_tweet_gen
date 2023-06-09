from tornado_sqlalchemy import SQLAlchemy
from alembic.config import Config
from sqlalchemy.orm import sessionmaker


config = Config("alembic.ini")
db = SQLAlchemy(config.get_main_option("sqlalchemy.url"))
make_session = sessionmaker(autocommit=False, autoflush=False, bind=db.get_engine())
datetime_format = "%b %d, %Y - %I:%M:%S %p"
