from unittest.mock import Mock

from ..app.services import extract as extract_service
from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_parses_json_response(monkeypatch):
    response = Mock()
    response.message.content = '["Email Dana", "Draft launch plan"]'
    monkeypatch.setattr(extract_service, "chat", Mock(return_value=response))

    items = extract_action_items_llm("Dana needs an email. Draft the launch plan.")

    assert items == ["Email Dana", "Draft launch plan"]


def test_extract_action_items_llm_falls_back_to_rules_on_bad_json(monkeypatch):
    response = Mock()
    response.message.content = "not json"
    monkeypatch.setattr(extract_service, "chat", Mock(return_value=response))

    items = extract_action_items_llm("- [ ] Set up database")

    assert items == ["Set up database"]


def test_extract_action_items_llm_handles_empty_array(monkeypatch):
    response = Mock()
    response.message.content = "[]"
    monkeypatch.setattr(extract_service, "chat", Mock(return_value=response))

    assert extract_action_items_llm("") == []
