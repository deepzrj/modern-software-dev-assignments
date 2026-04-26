from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip_required(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Field cannot be blank")
    return value


def _strip_optional(value: str | None) -> str | None:
    if value is None:
        return value
    return _strip_required(value)


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)

    _normalize_title = field_validator("title")(_strip_required)
    _normalize_content = field_validator("content")(_strip_required)


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotePatch(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None

    _normalize_title = field_validator("title")(_strip_optional)
    _normalize_content = field_validator("content")(_strip_optional)


class ActionItemCreate(BaseModel):
    description: str = Field(min_length=1)

    _normalize_description = field_validator("description")(_strip_required)


class ActionItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None

    _normalize_description = field_validator("description")(_strip_optional)


class ActionItemCommentCreate(BaseModel):
    body: str = Field(min_length=1)

    _normalize_body = field_validator("body")(_strip_required)


class ActionItemCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action_item_id: int
    body: str
    created_at: datetime
    updated_at: datetime
