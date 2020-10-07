import datetime

from slugify import slugify
from sqlalchemy.orm import relationship

from blog_pyramid.models.meta import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from blog_pyramid.models.category import posts_categories


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    intro = Column(String(100))
    body = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    slug = Column(String(40), unique=True)
    author = relationship('User', back_populates='posts')
    author_username = Column(String, ForeignKey('user.username'))
    categories = relationship('Category', secondary=posts_categories, back_populates='posts')

    def __init__(self, title):
        self.slug = slugify(title)
