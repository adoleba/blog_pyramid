from pyramid.view import view_config

from blog_pyramid.models import Post, Category
from blog_pyramid.services.categories import CategoryBlogService
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
        categories = CategoryBlogService.all(self.request)
        return categories

    @property
    def page(self):
        page = int(self.request.params.get('page', 1))
        return page

    @view_config(route_name='index', renderer='../templates/blog/posts.jinja2', permission='view')
    def index(self):
        title = "Welcome to our blog"
        posts = PostServiceBlog.all(request=self.request, page=self.page)
        return {'posts': posts, 'categories': self.categories, 'title': title}

    @view_config(route_name='blog_category_posts', renderer='../templates/blog/posts.jinja2', permission='view')
    def blog_category_posts(self):
        category_slug = self.request.matchdict['category_slug']
        category = self.request.dbsession.query(Category).filter_by(slug=category_slug).one()
        category_name = category.name
        posts = PostServiceBlog.by_category(request=self.request, page=self.page, category=category_name)
        title = "Posts from category " + category_name
        return {'title': title, 'categories': self.categories, 'posts': posts}

    @view_config(route_name='blog_user_posts', renderer='../templates/blog/posts.jinja2', permission='view')
    def blog_user_posts(self):
        username = self.request.matchdict['username']
        posts = PostServiceBlog.by_user(self.request, page=self.page, username=username)
        title = "Posts from user " + username
        return {'title': title, 'categories': self.categories, 'posts': posts}

    @view_config(route_name='post_page', renderer='../templates/blog/post_page.jinja2', permission='view')
    def post_page(self):
        return {'post': self.post,  'categories': self.categories}
