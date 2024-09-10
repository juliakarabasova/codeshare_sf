import uuid
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from starlette import status

from api.v1.auth import get_current_user
from db.db import db_dependency
from schemas.snippets import CodeSnippetResponse, CodeSnippetCreate, CodeSnippetUpdate
from models.code_snippets import CodeSnippets


code_router = APIRouter(prefix="/user", tags=['snippets'])


@code_router.get("/get_code/{snippet_uuid}", response_model=CodeSnippetResponse)
async def get_code(code_uuid: uuid.UUID, db: db_dependency):
    try:
        result = await db.execute(select(CodeSnippets).where(CodeSnippets.uuid == code_uuid))
        snippet = result.scalar_one_or_none()

        if snippet is None:
            raise HTTPException(status_code=404, detail="Snippet not found")
        return snippet
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Snippet not found")


@code_router.post("/snippet", response_model=CodeSnippetResponse)
async def create_snippet(
        snippet_data: CodeSnippetCreate,
        db: db_dependency,
        current_user: dict = Depends(get_current_user)
):
    """
    Add a new code snippet to the database. Only accessible to authorized users.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    new_snippet = CodeSnippets(
        snippet=snippet_data.snippet,
        uuid=uuid.uuid4()
    )

    db.add(new_snippet)
    await db.commit()
    await db.refresh(new_snippet)

    return new_snippet


@code_router.put("/snippet/{snippet_uuid}", response_model=CodeSnippetResponse)
async def update_snippet(
    snippet_uuid: uuid.UUID,
    snippet_data: CodeSnippetUpdate,
    db: db_dependency,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a code snippet by UUID. Only accessible to the snippet owner (authorized user).
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    result = await db.execute(select(CodeSnippets).where(CodeSnippets.uuid == snippet_uuid))
    snippet = result.scalar_one_or_none()

    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")

    # TODO
    # if snippet.owner_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to edit this snippet")

    snippet.snippet = snippet_data.snippet

    await db.commit()
    await db.refresh(snippet)

    return snippet


@code_router.delete("/snippet/{snippet_uuid}", response_model=dict)
async def delete_snippet(
    snippet_uuid: uuid.UUID,
    db: db_dependency,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a code snippet by UUID. Only accessible to the snippet owner (authorized user).
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    result = await db.execute(select(CodeSnippets).where(CodeSnippets.uuid == snippet_uuid))
    snippet = result.scalar_one_or_none()

    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")

    # TODO
    # if snippet.owner_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this snippet")

    await db.delete(snippet)
    await db.commit()

    return {"detail": "Snippet deleted successfully"}
