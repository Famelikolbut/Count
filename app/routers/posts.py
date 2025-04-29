from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_filtered_posts
from app.db import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse, PostQueryParams, PostListResponse

router = APIRouter()


@router.post("/posts", response_model=PostResponse)
async def create_post(
        post_data: PostCreate,
        session: AsyncSession = Depends(get_db)
):
    new_post = Post(category=post_data.category, content=post_data.content)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    word_count = dict(Counter(new_post.content.split()))

    return PostResponse(id=new_post.id, category=new_post.category, content=new_post.content, word_count=word_count)


@router.get("/posts", response_model=PostListResponse)
async def get_posts(query_params: PostQueryParams = Depends(), session: AsyncSession = Depends(get_db)):
    posts, total_count = await get_filtered_posts(
        session, category=query_params.category, keyword=query_params.keyword,
        limit=query_params.limit, offset=query_params.offset
    )

    posts_response = [
        PostResponse(
            id=post.id,
            category=post.category,
            content=post.content,
            word_count=dict(Counter(post.content.split()))
        )
        for post in posts
    ]

    return {"posts": posts_response, "total_count": total_count}