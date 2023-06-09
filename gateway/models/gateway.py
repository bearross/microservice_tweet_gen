from sqlalchemy import Column, String, TIMESTAMP, text, SMALLINT
from sqlalchemy.dialects.postgresql import UUID
import uuid
from settings import db

metadata = db.metadata


class HistoryModel(db.Model):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    status = Column(SMALLINT(), server_default=text("1"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

