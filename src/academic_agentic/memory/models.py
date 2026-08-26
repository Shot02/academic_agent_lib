from pydantic import BaseModel

class MemoryEntry(BaseModel):
    role: str
    content: str