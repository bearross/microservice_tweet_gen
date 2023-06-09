from alembic.config import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, INTEGER, FLOAT, text

config = Config("alembic.ini")
Base = declarative_base()
metadata = Base.metadata


class KeywordUrlStore(Base):
    __tablename__ = 'keyword_url_store'
    id = Column('Id', INTEGER(), primary_key=True)
    account_id = Column(String(length=36), index=True)
    keyword = Column("Keyword", String(64), nullable=False)
    url = Column('Url', String(256), nullable=False)
    position = Column('Position', FLOAT(), nullable=False)
    traffic = Column('Traffic', String(64), nullable=False)
    pa = Column('PA', FLOAT(), nullable=False)
    average_position = Column(FLOAT(), nullable=False)
    average_traffic = Column(FLOAT(), nullable=False)
    average_pa = Column(FLOAT(), nullable=False)
    weighted_value = Column('Weighted Value', FLOAT(), nullable=False)
    ownership_score = Column(FLOAT(), nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    update_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

