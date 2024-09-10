import uuid
from datetime import datetime
from pydantic import BaseModel


class CodeSnippetResponse(BaseModel):
    id: int
    snippet: str
    uuid: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True


class CodeSnippetCreate(BaseModel):
    snippet: str


class CodeSnippetUpdate(BaseModel):
    snippet: str
