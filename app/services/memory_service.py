from collections import defaultdict
from typing import List, Dict


# In-memory store: session_id -> message history
_memory_store: Dict[str, List[Dict[str, str]]] = defaultdict(list)

MAX_HISTORY = 6  # last 3 user + 3 assistant messages


def get_history(session_id: str) -> List[Dict[str, str]]:
    return _memory_store[session_id]


def add_message(session_id: str, role: str, content: str):
    _memory_store[session_id].append({
        "role": role,
        "content": content
    })

    # Keep only last N messages
    if len(_memory_store[session_id]) > MAX_HISTORY:
        _memory_store[session_id] = _memory_store[session_id][-MAX_HISTORY:]
