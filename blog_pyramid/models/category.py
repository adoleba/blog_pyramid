import datetime

from slugify import slugify
from sqlalchemy.orm import relationship

from blog_pyramid.models.meta import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table


posts_categories = Table('posts_categories', Base.metadata,
                         Column('category_id', Integer, ForeignKey('category.id')),
                         Column('post_id', Integer, ForeignKey('posts.id'))
                         )


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    description = Column(String(100))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    slug = Column(String(30), unique=True)
    posts = relationship('Post', secondary=posts_categories, back_populates='categories')

    def __init__(self, name):
        self.slug = slugify(name)
