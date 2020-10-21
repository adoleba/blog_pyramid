from blog_pyramid.models import User


class UserService:

    @classmethod
    def all(cls, request):
        return request.dbsession.query(User).order_by(User.username)
