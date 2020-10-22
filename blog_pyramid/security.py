from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated

from blog_pyramid.models.user import User
from blog_pyramid.services.users import UserService


class CustomAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.username

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user is not None:
            principals.append(Authenticated)
            principals.append(str(user.username))
            principals.append('role:' + user.role)
        return principals


def get_user(request):
    user_username = request.unauthenticated_userid
    if user_username is not None:
        user = request.dbsession.query(User).filter(User.username == user_username).first()
        return user


def includeme(config):
    settings = config.get_settings()
    authn_policy = CustomAuthenticationPolicy(settings['auth.secret'], hashalg='sha512')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
