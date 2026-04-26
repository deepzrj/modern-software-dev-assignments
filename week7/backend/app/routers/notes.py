from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import ActionItemRead, NoteCreate, NotePatch, NoteRead
from ..services.extract import extract_action_items

router = APIRouter(prefix="/notes", tags=["notes"])
SORT_FIELDS = {
    "created_at": Note.created_at,
    "updated_at": Note.updated_at,
    "title": Note.title,
    "id": Note.id,
}


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if sort_field not in SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f"Unsupported sort field: {sort_field}")
    stmt = stmt.order_by(order_fn(SORT_FIELDS[sort_field]))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.post(
    "/{note_id}/extract-action-items", response_model=list[ActionItemRead], status_code=201
)
def extract_note_action_items(note_id: int, db: Session = Depends(get_db)) -> list[ActionItemRead]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    items = [
        ActionItem(description=description, completed=False)
        for description in extract_action_items(note.content)
    ]
    db.add_all(items)
    db.flush()
    for item in items:
        db.refresh(item)
    return [ActionItemRead.model_validate(item) for item in items]


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    return Response(status_code=204)
