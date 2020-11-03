from pyramid.view import view_config

from blog_pyramid.models import Post
from blog_pyramid.services.categories import CategoryService
from blog_pyramid.services.posts import PostService


class PostsViews:
    def __init__(self, request):
        self.request = request

    @property
    def slug(self):
        slug = self.request.matchdict['slug']
        return slug

    @property
    def post(self):
        post = self.request.dbsession.query(Post).filter_by(slug=self.slug).one()
        return post

    @property
    def categories(self):
        categories = CategoryService.all(self.request)
        return categories

    @view_config(route_name='index', renderer='../templates/blog/posts.jinja2', permission='view')
    def index(self):
        posts = PostService.all(self.request)
        return {'posts': posts, 'categories': self.categories}

    @view_config(route_name='post_page', renderer='../templates/blog/post_page.jinja2', permission='view')
    def post_page(self):
        return {'post': self.post,  'categories': self.categories}
