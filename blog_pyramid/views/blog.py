from pyramid.view import view_config

from blog_pyramid.models import Post, Category
from blog_pyramid.services.categories import CategoryService
from blog_pyramid.services.posts import PostServiceBlog


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
        title = "Welcome to our blog"
        posts = PostServiceBlog.all(self.request)
        return {'posts': posts, 'categories': self.categories, 'title': title}#, 'category_slug': category_slug}

    @view_config(route_name='blog_category_posts', renderer='../templates/blog/posts.jinja2', permission='view')
    def blog_category_posts(self):
        category_slug = self.request.matchdict['category_slug']
        category = self.request.dbsession.query(Category).filter_by(slug=category_slug).one()
        category_name = category.name
        posts = PostServiceBlog.by_category(self.request, category_name)
        title = "Posts from category " + category_name
        return {'title': title, 'categories': self.categories, 'posts': posts}

    @view_config(route_name='post_page', renderer='../templates/blog/post_page.jinja2', permission='view')
    def post_page(self):

        return {'post': self.post,  'categories': self.categories}
