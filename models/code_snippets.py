import uuid
from datetime import datetime
from sqlalchemy import String, Column, Integer, TIMESTAMP, UUID
from .base import Base


class CodeSnippets(Base):
    __tablename__ = "codesnippet"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    snippet = Column(String(256))
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
