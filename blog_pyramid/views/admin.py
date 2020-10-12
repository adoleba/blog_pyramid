import deform
from deform import Form
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from blog_pyramid.forms.post import PostForm
from blog_pyramid.services.posts import PostService


class AdminViews:
    def __init__(self, request):
        self.request = request

    @property
    def post_form(self):
        post_form = PostForm()
        submit = deform.Button(name='Zapisz', css_class='btn btn-info')
        cancel = deform.Button(name='Anuluj', css_class='btn btn-inverse')
        return Form(post_form, buttons=(submit, cancel))

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
        form = self.post_form.render()

        if 'Zapisz' in self.request.params:
            post_title = self.request.params.get('title')
            post_intro = self.request.params.get('intro')
            post_body = self.request.params.get('body')
            post_category = self.request.params.get('categories')
            url = self.request.route_url('admin_posts')
            return HTTPFound(location=url)

        return {'title': title, 'form': form}
