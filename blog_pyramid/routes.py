from pyramid.security import Allow, Deny

class AdminFactory:
    def __init__(self, request):
        self.request = request
        self.__acl__ = [
            (Allow, 'role:admin', 'admin'),
        ]

class UserFactory:
    def __init__(self, request):
        self.request = request
        self.__acl__ = [
            (Allow, 'role:admin', 'user'),
            (Allow, 'role:editor', 'user'),
        ]

def admin_factory(request):
    return AdminFactory(request)


def user_factory(request):
    return UserFactory(request)


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('admin', '/admin', factory=user_factory)
    config.add_route('login', '/admin/login', factory=user_factory)
    config.add_route('logout', '/admin/logout', factory=user_factory)
    config.add_route('admin_posts', '/admin/posts', factory=user_factory)
    config.add_route('admin_categories', '/admin/categories', factory=user_factory)
    config.add_route('admin_users', '/admin/users', factory=admin_factory)
    config.add_route('category_create', '/admin/categories/create', factory=user_factory)
    config.add_route('category_edit', '/admin/categories/{slug}/edit', factory=user_factory)
    config.add_route('category_delete', '/admin/categories/{slug}/delete', factory=user_factory)
    config.add_route('category_delete_confirmed', '/admin/categories/{slug}/delete/confirmed', factory=user_factory)
    config.add_route('post_create', '/admin/posts/create', factory=user_factory)
    config.add_route('post_edit', '/admin/posts/{slug}/edit', factory=user_factory)
    config.add_route('post_delete', '/admin/posts/{slug}/delete', factory=user_factory)
    config.add_route('post_delete_confirmed', '/admin/posts/{slug}/delete/confirmed', factory=user_factory)
    config.add_route('user_register', '/admin/users/register', factory=admin_factory)
    config.add_route('user_edit', '/admin/users/{username}/edit', factory=admin_factory)
    config.add_route('user_email_edit', '/admin/users/{username}/email_edit', factory=admin_factory)
