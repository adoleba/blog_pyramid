import datetime

from slugify import slugify

from blog_pyramid.models.meta import Base
from sqlalchemy import Column, Integer, String, DateTime


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True)
    description = Column(String(100))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    slug = Column(String(30), unique=True)

    def __init__(self, name, description):
        self.slug = slugify(name)
        self.name = name
        self.description = description
