from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - Write tests!
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "Write tests!" in items
    assert "Ship it!" in items
