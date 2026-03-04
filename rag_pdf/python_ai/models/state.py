from typing import List, Optional
from pydantic import BaseModel
from langchain_core.messages import BaseMessage

class GraphState(BaseModel):
    messages: List[BaseMessage] = []
    summary: Optional[str] = None