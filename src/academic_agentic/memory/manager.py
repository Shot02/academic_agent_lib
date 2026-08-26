from collections import defaultdict
from academic_agentic.memory.models import MemoryEntry

class MemoryManager:
    """Small replaceable conversation-memory layer; use a durable store in production."""
    def __init__(self, window: int = 16) -> None:
        self.window = window
        self._sessions: dict[str, list[MemoryEntry]] = defaultdict(list)
    
    def recent(self, session_id: str) -> list[str]:
        return [f"{x.role}: {x.content}" for x in self._sessions[session_id][-self.window:]]
    
    def append(self, session_id: str, role: str, content: str) -> None:
        self._sessions[session_id].append(MemoryEntry(role=role, content=content))
        self._sessions[session_id] = self._sessions[session_id][-self.window:]