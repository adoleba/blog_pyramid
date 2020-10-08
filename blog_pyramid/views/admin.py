from pyramid.view import view_config


class AdminViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='admin', renderer='../templates/admin/base.jinja2')
    def admin(self):
        title = 'Admin panel'
        return {'title': title}

    @view_config(route_name='admin_posts', renderer='../templates/admin/posts/posts_list.jinja2')
    def admin_posts(self):
        title = 'Posts list'
        return {'title': title}
