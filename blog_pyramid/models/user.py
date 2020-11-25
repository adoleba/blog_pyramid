import datetime

from passlib.apps import custom_app_context as user_pwd_context
from sqlalchemy import Column, Integer, String, DateTime

from blog_pyramid.models.meta import Base


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
    role = Column(String(10), default='editor', nullable=True)

    def verify_password(self, password):
        if password == self.password:
            self.set_password(password)

        return user_pwd_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = user_pwd_context.encrypt(password)
        self.password = password_hash
