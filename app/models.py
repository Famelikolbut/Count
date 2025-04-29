# app/models.py
from sqlalchemy import Column, Integer, String
from app.db import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, index=True)
    content = Column(String)

    def __repr__(self):
        return f"<Post(id={self.id}, category={self.category}, content={self.content})>"
