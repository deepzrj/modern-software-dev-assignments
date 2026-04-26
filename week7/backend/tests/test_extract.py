from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_action_items_recognizes_more_patterns_and_deduplicates():
    text = """
    1. Follow-up: email Ana
    * Next step: schedule launch review
    - Owner: Priya due: Friday
    - Review deployment plan
    - review deployment plan
    Informational only
    """.strip()

    items = extract_action_items(text)

    assert items == [
        "Follow-up: email Ana",
        "Next step: schedule launch review",
        "Owner: Priya due: Friday",
        "Review deployment plan",
    ]
