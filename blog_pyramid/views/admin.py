from pyramid.view import view_config

from blog_pyramid.models import Post
from blog_pyramid.services.posts import PostService


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
        posts = PostService.all(request=self.request)
        return {'title': title, 'posts': posts}

    @view_config(route_name='post_create', renderer='../templates/admin/posts/post_create.jinja2')
    def post_create(self):
        title = 'Create a post'
        return {'title': title}
