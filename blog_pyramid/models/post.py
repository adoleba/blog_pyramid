import datetime

from slugify import slugify
from sqlalchemy import Column, Integer, String, DateTime

from blog_pyramid.models.meta import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    intro = Column(String(100))
    body = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    slug = Column(String(40), unique=True)
    category = Column(String(30))
    author = Column(String(30))

    def __init__(self, title, intro, body, category, author):
        self.slug = slugify(title)
        self.title = title
        self.intro = intro
        self.body = body
        self.category = category
        self.author = author
