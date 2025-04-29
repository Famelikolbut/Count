import re

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post
from app.schemas import PostResponse


def count_words(text: str) -> dict:
    words = re.findall(r'\w+', text.lower())
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq


async def get_filtered_posts(
        session: AsyncSession,
        category: str = None,
        keyword: str = None,
        limit: int = 10,
        offset: int = 0
):
    base_query = select(Post)

    if category:
        base_query = base_query.where(Post.category == category)

    if keyword:
        base_query = base_query.where(Post.content.ilike(f"%{keyword}%"))

    count_query = select(func.count()).select_from(base_query.subquery())
    total_count = (await session.execute(count_query)).scalar_one()

    paginated_query = base_query.offset(offset).limit(limit)
    result = await session.stream(paginated_query)

    posts = []
    async for row in result.scalars():
        word_count = count_words(row.content)
        post_data = PostResponse(
            id=row.id,
            category=row.category,
            content=row.content,
            word_count=word_count
        )
        posts.append(post_data)

    return posts, total_count
