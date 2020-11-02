from blog_pyramid.models import User


class UserService:

    @classmethod
    def all(cls, request):
        return request.dbsession.query(User).order_by(User.username)

    @classmethod
    def by_email(cls, email, request):
        return request.dbsession.query(User).filter(User.email == email).first()
