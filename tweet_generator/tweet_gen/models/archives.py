import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, text, SMALLINT, INTEGER, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()
metadata = Base.metadata

statuses = {
    "20": "Parsing",
    "21": "Collecting texts",
    "22": "Fine-tuning",
    "0": "Active"
}


def status_text(status):
    return statuses[str(status)]


class Archive(Base):
    __tablename__ = 'tweet_gen_archives'

    id = Column(INTEGER(), primary_key=True)
    account_id = Column(UUID(as_uuid=True), index=True)

    filename = Column(String(255))
    status = Column(SMALLINT(), server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text('CURRENT_TIMESTAMP'))


class Username(Base):
    __tablename__ = 'tweet_gen_usernames'

    id = Column(INTEGER(), primary_key=True)
    archive_id = Column(INTEGER(), ForeignKey("tweet_gen_archives.id"))
    username = Column(String(255))
    status = Column(SMALLINT(), server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.datetime.now)


class TweetURL(Base):
    __tablename__ = 'tweet_gen_urls'

    id = Column(INTEGER(), primary_key=True)
    account_id = Column(UUID(as_uuid=True), index=True)
    url = Column(String(255))
    status = Column(SMALLINT(), server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text('CURRENT_TIMESTAMP'))


class Tweet(Base):
    __tablename__ = 'tweet_gen_tweets'

    id = Column(INTEGER(), primary_key=True)
    account_id = Column(UUID(as_uuid=True), index=True)
    url_id = Column(INTEGER(), ForeignKey("tweet_gen_urls.id"))
    tweet = Column(Text())
    status = Column(SMALLINT(), server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text('CURRENT_TIMESTAMP'))
