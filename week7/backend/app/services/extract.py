import re

ACTION_PREFIX_RE = re.compile(r"^(?:todo|action|follow[- ]?up|next step|task)\s*:\s*(.+)$", re.I)
ASSIGNEE_RE = re.compile(r"\b(?:assign(?:ed)? to|owner)\s*:\s*([A-Za-z][\w .-]*)", re.I)
DUE_RE = re.compile(r"\b(?:due|by)\s*:\s*([A-Za-z0-9, /\-]+)", re.I)
IMPERATIVE_STARTS = (
    "add",
    "call",
    "create",
    "email",
    "fix",
    "follow up",
    "implement",
    "review",
    "schedule",
    "send",
    "ship",
    "update",
)


def _clean_line(line: str) -> str:
    return re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()


def extract_action_items(text: str) -> list[str]:
    lines = [_clean_line(line) for line in text.splitlines() if line.strip()]
    results: list[str] = []
    seen: set[str] = set()
    for line in lines:
        normalized = line.lower()
        prefix_match = ACTION_PREFIX_RE.match(line)
        if prefix_match:
            item = line
        elif line.endswith("!"):
            item = line
        elif any(normalized.startswith(verb) for verb in IMPERATIVE_STARTS):
            item = line
        elif ASSIGNEE_RE.search(line) or DUE_RE.search(line):
            item = line
        else:
            continue

        if item and item.lower() not in seen:
            seen.add(item.lower())
            results.append(item)
    return results
