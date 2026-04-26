from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, ActionItemComment
from ..schemas import (
    ActionItemCommentCreate,
    ActionItemCommentRead,
    ActionItemCreate,
    ActionItemPatch,
    ActionItemRead,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])
SORT_FIELDS = {
    "created_at": ActionItem.created_at,
    "updated_at": ActionItem.updated_at,
    "description": ActionItem.description,
    "completed": ActionItem.completed,
    "id": ActionItem.id,
}


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if sort_field not in SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f"Unsupported sort field: {sort_field}")
    stmt = stmt.order_by(order_fn(SORT_FIELDS[sort_field]))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ActionItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(
    item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)
) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    db.delete(item)
    return Response(status_code=204)


@router.get("/{item_id}/comments", response_model=list[ActionItemCommentRead])
def list_comments(item_id: int, db: Session = Depends(get_db)) -> list[ActionItemCommentRead]:
    if not db.get(ActionItem, item_id):
        raise HTTPException(status_code=404, detail="Action item not found")
    stmt = (
        select(ActionItemComment)
        .where(ActionItemComment.action_item_id == item_id)
        .order_by(asc(ActionItemComment.created_at))
    )
    comments = db.execute(stmt).scalars().all()
    return [ActionItemCommentRead.model_validate(comment) for comment in comments]


@router.post("/{item_id}/comments", response_model=ActionItemCommentRead, status_code=201)
def create_comment(
    item_id: int,
    payload: ActionItemCommentCreate,
    db: Session = Depends(get_db),
) -> ActionItemCommentRead:
    if not db.get(ActionItem, item_id):
        raise HTTPException(status_code=404, detail="Action item not found")
    comment = ActionItemComment(action_item_id=item_id, body=payload.body)
    db.add(comment)
    db.flush()
    db.refresh(comment)
    return ActionItemCommentRead.model_validate(comment)
