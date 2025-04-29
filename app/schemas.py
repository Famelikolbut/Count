from typing import Dict
from typing import List, Optional

from pydantic import BaseModel


class PostResponse(BaseModel):
    id: int
    category: str
    content: str
    word_count: Dict[str, int]

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total_count: int

    class Config:
        orm_mode = True


class PostQueryParams(BaseModel):
    category: Optional[str] = None
    keyword: Optional[str] = None
    limit: int = 10
    offset: int = 0


class PostCreate(BaseModel):
    category: str
    content: str
