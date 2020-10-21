import datetime

from sqlalchemy.orm import relationship

from blog_pyramid.models.meta import Base
from sqlalchemy import Column, Integer, String, DateTime, Index, ForeignKey


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True)
    email = Column(String(30), unique=True)
    password = Column(String(30))
    about = Column(String(100))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    firstname = Column(String(30))
    lastname = Column(String(30))
    posts = relationship('Post', back_populates='author')

