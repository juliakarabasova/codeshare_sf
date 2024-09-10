from sqlalchemy.future import select

from db.db import db_dependency
from models.code_snippets import CodeSnippets


async def get_snippet_by_id(db: db_dependency, code_id: int):
    result = await db.execute(select(CodeSnippets).filter(CodeSnippets.id == code_id))
    return result.scalars().first()


async def get_codes(db: db_dependency, skip: int = 0, limit: int = 10):
    result = await db.execute(select(CodeSnippets).offset(skip).limit(limit))
    return result.scalars().all()


async def add_snippet(db: db_dependency, code: str):
    snippet_object = CodeSnippets(snippet=code)
    db.add(snippet_object)
    await db.commit()
    await db.refresh(snippet_object)

    return snippet_object


async def update_code(db: db_dependency, code_id: int, code: str):
    snippet_object = await get_snippet_by_id(db, code_id)
    if snippet_object:
        snippet_object.snippet = code
        await db.commit()
        await db.refresh(snippet_object)
    return snippet_object


async def delete_code(db: db_dependency, code_id: int):
    snippet_object = await get_snippet_by_id(db, code_id)
    if snippet_object:
        await db.delete(snippet_object)
        await db.commit()
    return snippet_object
