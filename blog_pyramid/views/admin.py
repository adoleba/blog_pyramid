import datetime
from functools import partial

import deform
from deform import Form, ValidationFailure
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
from slugify import slugify

from blog_pyramid.forms.category import CategoryForm, validate_unique_name
from blog_pyramid.forms.post import get_post_form, validate_unique_title
from blog_pyramid.forms.user import get_user_register_form, UserEditForm, get_user_email_edit_form, LoginForm
from blog_pyramid.models import Post, User
from blog_pyramid.models.category import Category
from blog_pyramid.services.categories import CategoryService
from blog_pyramid.services.posts import PostService
from blog_pyramid.services.users import UserService


@view_config(route_name='admin', renderer='../templates/admin/base.jinja2', permission='user')
def admin(request):
    title = 'Admin panel'
    return {'title': title}


@view_config(route_name='login', renderer='../templates/admin/login.jinja2')
def login(request):
    title = 'Login'
    form = LoginForm()
    email = request.POST.get('email')
    error = ''
    if email:
        user = UserService.by_email(email, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.username)
            return HTTPFound(location=request.route_url('admin'), headers=headers)
        error = 'Incorrect email or password'
    return {'title': title, 'form': form, 'error': error}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'), headers=headers)


class PostsViews:
    def __init__(self, request):
        self.request = request

    @property
    def post_form(self):
        post_form = get_post_form(self.request.dbsession, validator=partial(validate_unique_title, dbsession=self.request.dbsession)).bind(request=self.request)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(post_form, buttons=(submit, cancel))

    @view_config(route_name='admin_posts', renderer='../templates/admin/posts/posts_list.jinja2', permission='user')
    def admin_posts(self):
        title = 'Posts list'
        page = int(self.request.params.get('page', 1))
        paginator = PostService.get_paginator(request=self.request, page=page)
        return {'title': title, 'paginator': paginator}

    @view_config(route_name='post_create', renderer='../templates/admin/posts/post_create_edit.jinja2', permission='user')
    def post_create(self):
        title = 'Create a post'
        form = self.post_form

        if 'Save' in self.request.params:
            post_title = self.request.params.get('title')
            post_intro = self.request.params.get('intro')
            post_body = self.request.params.get('body')
            post_category = self.request.params.get('category')
            controls = self.request.POST.items()

            try:
                form.validate(controls)
                new_post = Post(title=post_title, intro=post_intro, body=post_body, category=post_category,
                                author=self.request.user.username)
                self.request.dbsession.add(new_post)

                url = self.request.route_url('admin_posts')
                return HTTPFound(location=url)

            except ValidationFailure as e:
                return {'form': e.render()}

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_posts'))

        return {'title': title, 'form': form.render()}

    @view_config(route_name='post_edit', renderer='../templates/admin/posts/post_create_edit.jinja2', permission='user')
    def post_edit(self):
        title = 'Edit a post'
        slug = self.request.matchdict['slug']
        post = self.request.dbsession.query(Post).filter_by(slug=slug).one()
        post_as_dict = post.__dict__
        form = self.post_form.render(appstruct=post_as_dict)
        url = self.request.route_url('post_edit', slug=post.slug)

        if 'Save' in self.request.params:
            new_post_title = self.request.params.get('title')
            new_post_intro = self.request.params.get('intro')
            new_post_body = self.request.params.get('body')
            new_post_category = self.request.params.get('category')
            edited = datetime.datetime.utcnow()
            new_post_slug = slugify(new_post_title)
            controls = self.request.POST.items()
            form_to_validate = self.post_form

            try:
                form_to_validate.validate(controls)

                self.request.dbsession.query(Post).filter(Post.slug == slug) \
                .update({'slug': new_post_slug, 'title': new_post_title, 'intro': new_post_intro, 'body': new_post_body,
                         'category': new_post_category, 'edited': edited})

                url = self.request.route_url('admin_posts')
                return HTTPFound(location=url)

            except ValidationFailure as e:
                return {'form': e.render()}

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_posts'))

        return {'title': title, 'form': form, 'url': url}

    @view_config(route_name='post_delete', renderer='../templates/admin/posts/post_delete.jinja2', permission='user')
    def post_delete(self):
        title = 'Delete post'
        slug = self.request.matchdict['slug']
        post = self.request.dbsession.query(Post).filter_by(slug=slug).one()

        return {'title': title, 'post': post}

    @view_config(route_name='post_delete_confirmed', renderer='../templates/admin/categories/category_delete.jinja2', permission='user')
    def post_delete_confirmed(self):
        slug = self.request.matchdict['slug']
        self.request.dbsession.query(Post).filter(Post.slug == slug).delete()

        return HTTPFound(location=self.request.route_url('admin_posts'))


class CategoriesViews:
    def __init__(self, request):
        self.request = request

    @property
    def category_form(self):
        category_form = CategoryForm(validator=partial(validate_unique_name, dbsession=self.request.dbsession)).bind(request=self.request)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(category_form, buttons=(submit, cancel, ))

    @view_config(route_name='admin_categories', renderer='../templates/admin/categories/categories_list.jinja2', permission='user')
    def admin_categories(self):
        title = 'Categories list'
        page = int(self.request.params.get('page', 1))
        paginator = CategoryService.get_paginator(request=self.request, page=page)
        return {'title': title, 'paginator': paginator}

    @view_config(route_name='category_create', renderer='../templates/admin/categories/category_create_edit.jinja2', permission='user')
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

    @view_config(route_name='category_edit', renderer='../templates/admin/categories/category_create_edit.jinja2', permission='user')
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
            controls = self.request.POST.items()
            form_to_validate = self.category_form

            try:
                form_to_validate.validate(controls)
                self.request.dbsession.query(Category).filter(Category.slug == slug)\
                .update({'slug': new_category_slug, 'description': new_category_description, 'name': new_category_name})

                url = self.request.route_url('admin_categories')
                return HTTPFound(location=url)

            except ValidationFailure as e:
                return {'form': e.render()}

        if 'Cancel' in self.request.params:
            return HTTPFound(location=self.request.route_url('admin_categories'))

        return {'title': title, 'form': form, 'url': url}

    @view_config(route_name='category_delete', renderer='../templates/admin/categories/category_delete.jinja2', permission='user')
    def category_delete(self):
        title = 'Delete category'
        slug = self.request.matchdict['slug']
        category = self.request.dbsession.query(Category).filter_by(slug=slug).one()

        return {'title': title, 'category': category}

    @view_config(route_name='category_delete_confirmed', renderer='../templates/admin/categories/category_delete.jinja2', permission='user')
    def category_delete_confirmed(self):
        slug = self.request.matchdict['slug']
        self.request.dbsession.query(Category).filter(Category.slug == slug).delete()

        return HTTPFound(location=self.request.route_url('admin_categories'))


class UserViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='admin_users', renderer='../templates/admin/users/users_list.jinja2', permission='admin')
    def admin_users(self):
        title = 'Users list'
        users = UserService.all(request=self.request)
        return {'title': title, 'users': users}

    @view_config(route_name='user_register', renderer='../templates/admin/users/user_register.jinja2', permission='admin')
    def user_register(self):
        title = 'Register new user'
        form = get_user_register_form(self.request.POST, self.request.dbsession)
        if self.request.method == "POST" and form.validate():
            new_user = User(username=form.username.data, email=form.email.data, firstname=form.firstname.data,
                            lastname=form.lastname.data, about=form.about.data)
            new_user.set_password(form.password.data.encode('utf8'))
            self.request.dbsession.add(new_user)
            return HTTPFound(location=self.request.route_url('admin_users'))
        return {'title': title, 'form': form}

    @view_config(route_name='user_edit', renderer='../templates/admin/users/user_edit.jinja2', permission='admin')
    def user_edit(self):
        title = 'Edit user'
        form = UserEditForm(self.request.POST)
        username = self.request.matchdict['username']

        user = self.request.dbsession.query(User).filter_by(username=username).one()
        form.lastname.data = user.lastname
        form.firstname.data = user.firstname
        form.about.data = user.about

        if self.request.method == "POST" and form.validate():
            new_lastname = self.request.params.get('lastname')
            new_about = self.request.params.get('about')
            new_firstname = self.request.params.get('firstname')

            self.request.dbsession.query(User).filter(User.username == username) \
                .update({'firstname': new_firstname, 'lastname': new_lastname, 'about': new_about})

            return HTTPFound(location=self.request.route_url('admin_users'))

        return {'title': title, 'form': form, 'username': username}

    @view_config(route_name='user_email_edit', renderer='../templates/admin/users/user_edit_email.jinja2', permission='admin')
    def user_email_edit(self):
        title = 'Edit email'
        form = get_user_email_edit_form(self.request.POST, self.request.dbsession)
        username = self.request.matchdict['username']

        user = self.request.dbsession.query(User).filter_by(username=username).one()

        if self.request.method == "POST":
            new_email = self.request.params.get('email')
            if new_email == user.email:
                return HTTPFound(location=self.request.route_url('admin_users'))

            if form.validate():
                self.request.dbsession.query(User).filter(User.username == username).update({'email': new_email})
                return HTTPFound(location=self.request.route_url('admin_users'))

        return {'title': title, 'form': form, 'username': username}


@forbidden_view_config()
def forbidden_view(request):
    return HTTPFound(location=request.route_url('login'))
