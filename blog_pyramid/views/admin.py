import datetime
from functools import partial

import colander
import transaction

import deform
from deform import Form, ValidationFailure
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from slugify import slugify

from blog_pyramid.forms.category import CategoryForm, validate_unique_name
from blog_pyramid.forms.post import get_post_form
from blog_pyramid.models import Post
from blog_pyramid.models.category import Category
from blog_pyramid.services.categories import CategoryService
from blog_pyramid.services.posts import PostService


@view_config(route_name='admin', renderer='../templates/admin/base.jinja2')
def admin(request):
    title = 'Admin panel'
    return {'title': title}


class PostsViews:
    def __init__(self, request):
        self.request = request

    @property
    def post_form(self):
        post_form = get_post_form(self.request.dbsession)
        submit = deform.Button(name='Create', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(post_form, buttons=(submit, cancel))

    @view_config(route_name='admin_posts', renderer='../templates/admin/posts/posts_list.jinja2')
    def admin_posts(self):
        title = 'Posts list'
        posts = PostService.all(request=self.request)
        return {'title': title, 'posts': posts}

    @view_config(route_name='post_create', renderer='../templates/admin/posts/post_create_edit.jinja2')
    def post_create(self):
        title = 'Create a post'
        form = self.post_form.render()

        if 'Create' in self.request.params:
            post_title = self.request.params.get('title')
            post_intro = self.request.params.get('intro')
            post_body = self.request.params.get('body')
            post_category = self.request.params.get('category')

            new_post = Post(title=post_title, intro=post_intro, body=post_body, category=post_category)
            self.request.dbsession.add(new_post)

            url = self.request.route_url('admin_posts')
            return HTTPFound(location=url)

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_posts'))

        return {'title': title, 'form': form}

    @view_config(route_name='post_edit', renderer='../templates/admin/posts/post_create_edit.jinja2')
    def post_edit(self):
        title = 'Edit a post'

        return {'title': title}

    @view_config(route_name='post_delete', renderer='../templates/admin/posts/post_delete.jinja2')
    def post_delete(self):
        title = 'Delete a post'

        return {'title': title}


class CategoriesViews:
    def __init__(self, request):
        self.request = request

    @property
    def category_form(self):
        category_form = CategoryForm(validator=partial(validate_unique_name, dbsession=self.request.dbsession)).bind(request=self.request) # validator = partial(validate_unique_name, dbsession)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(category_form, buttons=(submit, cancel, ))

    @view_config(route_name='admin_categories', renderer='../templates/admin/categories/categories_list.jinja2')
    def admin_categories(self):
        title = 'Categories list'
        categories = CategoryService.all(request=self.request)
        return {'title': title, 'categories': categories}

    @view_config(route_name='category_create', renderer='../templates/admin/categories/category_create_edit.jinja2')
    def category_create(self):
        title = 'Create a category'

        form = self.category_form

        if 'Save' in self.request.params:
            name = self.request.params.get('name')
            description = self.request.params.get('description')
            controls = self.request.POST.items()

            try:
                form.validate(controls)
                new_category = Category(name=name, description=description)

                self.request.dbsession.add(new_category)

                url = self.request.route_url('admin_categories')
                return HTTPFound(location=url)

            except ValidationFailure as e:
                return {'form': e.render()}

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_categories'))

        return {'title': title, 'form': form.render()}

    @view_config(route_name='category_edit', renderer='../templates/admin/categories/category_create_edit.jinja2')
    def category_edit(self):
        title = 'Edit a category'

        slug = self.request.matchdict['slug']
        category = self.request.dbsession.query(Category).filter_by(slug=slug).one()
        category_as_dict = category.__dict__
        form = self.category_form.render(appstruct=category_as_dict)
        url = self.request.route_url('category_edit', slug=category.slug)

        if 'Save' in self.request.params:
            new_category_name = self.request.params.get('name')
            new_category_description = self.request.params.get('description')
            new_category_slug = slugify(new_category_name)
            self.request.dbsession.query(Category).filter(Category.slug == slug)\
                .update({'slug': new_category_slug, 'description': new_category_description, 'name': new_category_name})

            url = self.request.route_url('admin_categories')
            return HTTPFound(location=url)

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_categories'))

        return {'title': title, 'form': form, 'url': url}

    @view_config(route_name='category_delete', renderer='../templates/admin/categories/category_delete.jinja2')
    def category_delete(self):
        title = 'Delete category'
        slug = self.request.matchdict['slug']
        category = self.request.dbsession.query(Category).filter_by(slug=slug).one()

        return {'title': title, 'category': category}

    @view_config(route_name='category_delete_confirmed', renderer='../templates/admin/categories/category_delete.jinja2')
    def category_delete_confirmed(self):
        slug = self.request.matchdict['slug']
        self.request.dbsession.query(Category).filter(Category.slug == slug).delete()

        return HTTPFound(location=self.request.route_url('admin_categories'))
