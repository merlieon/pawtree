from pydantic import BaseModel
from .pedigree import PedigreeNode

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

class ChatResponse(BaseModel):
    reply: str
    pedigree: PedigreeNode | None = None
