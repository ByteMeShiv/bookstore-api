from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    title: str
    author: str

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
