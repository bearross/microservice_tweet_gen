from sqlalchemy import Column, String, TIMESTAMP, text, SMALLINT, ForeignKey, INTEGER
from sqlalchemy.dialects.postgresql import UUID
import uuid
from settings import db
import secrets

metadata = db.metadata


def generate_secret():
    return secrets.token_urlsafe(64)


class APIKeys(db.Model):
    __tablename__ = 'api_keys'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), index=True)

    name = Column(String(255), nullable=False)
    secret = Column(String(255), nullable=False, default=generate_secret())

    status = Column(SMALLINT(), server_default=text("0"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class KeyHistory(db.Model):
    __tablename__ = 'key_history'
    id = Column(INTEGER(), primary_key=True)
    key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"))
    account_id = Column(UUID(as_uuid=True), index=True)

    type = Column(SMALLINT(), server_default=text("0"))

    status = Column(SMALLINT(), server_default=text("1"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
