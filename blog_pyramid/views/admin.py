import datetime
from functools import partial

import deform
from deform import Form, ValidationFailure
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config

from blog_pyramid.forms.category import CategoryCreateForm, validate_unique_name, CategoryEditForm
from blog_pyramid.forms.post import get_post_form, validate_unique_title, get_edit_post_form
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


@view_config(route_name='login', renderer='../templates/admin/login.jinja2', permission='view')
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


@view_config(route_name='logout', permission='view')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('login'), headers=headers)


class PostsViews:
    def __init__(self, request):
        self.request = request

    @property
    def post_create_form(self):
        post_create_form = get_post_form(self.request.dbsession, validator=partial(validate_unique_title, dbsession=self.request.dbsession)).bind(request=self.request)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(post_create_form, buttons=(submit, cancel))

    @property
    def post_edit_form(self):
        post_edit_form = get_edit_post_form(self.request.dbsession)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(post_edit_form, buttons=(submit, cancel))

    @property
    def logged_user(self):
        logged_user = self.request.dbsession.query(User).filter_by(username=self.request.authenticated_userid).one()
        return logged_user

    @property
    def slug(self):
        slug = self.request.matchdict['slug']
        return slug

    @property
    def post(self):
        post = self.request.dbsession.query(Post).filter_by(slug=self.slug).one()
        return post

    @view_config(route_name='admin_posts', renderer='../templates/admin/posts/posts_list.jinja2', permission='user')
    def admin_posts(self):
        title = 'Posts list'
        page = int(self.request.params.get('page', 1))
        paginator = PostService.get_paginator(request=self.request, page=page)
        return {'title': title, 'paginator': paginator}

    @view_config(route_name='post_create', renderer='../templates/admin/posts/post_create.jinja2', permission='user')
    def post_create(self):
        title = 'Create a post'
        form = self.post_create_form

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

    @view_config(route_name='post_edit', renderer='../templates/admin/posts/post_edit.jinja2', permission='user')
    def post_edit(self):

        post_as_dict = self.post.__dict__
        form = self.post_edit_form.render(appstruct=post_as_dict)

        if self.logged_user.role == 'admin' or self.request.authenticated_userid == self.post.author:

            if 'Save' in self.request.params:
                new_post_intro = self.request.params.get('intro')
                new_post_body = self.request.params.get('body')
                new_post_category = self.request.params.get('category')
                controls = self.request.POST.items()
                edited = datetime.datetime.utcnow()
                form_to_validate = self.post_edit_form

                try:
                    form_to_validate.validate(controls)
                    self.request.dbsession.query(Post).filter(Post.slug == self.slug) \
                    .update({'intro': new_post_intro, 'body': new_post_body, 'category': new_post_category, 'edited': edited})

                    url = self.request.route_url('admin_posts')
                    return HTTPFound(location=url)

                except ValidationFailure as e:
                    return {'form': e.render(), 'post': self.post}

            if 'Cancel' in self.request.params:
                return HTTPFound(location=self.request.route_url('admin_posts'))
        else:
            return HTTPForbidden()

        return {'form': form, 'post': self.post}

    @view_config(route_name='post_delete', renderer='../templates/admin/posts/post_delete.jinja2', permission='user')
    def post_delete(self):
        if self.logged_user.role == 'admin' or self.request.authenticated_userid == self.post.author:
            title = 'Delete post'
            return {'title': title, 'post': self.post}
        else:
            return HTTPForbidden()

    @view_config(route_name='post_delete_confirmed', renderer='../templates/admin/categories/category_delete.jinja2', permission='user')
    def post_delete_confirmed(self):
        self.request.dbsession.query(Post).filter(Post.slug == self.slug).delete()

        return HTTPFound(location=self.request.route_url('admin_posts'))


class CategoriesViews:
    def __init__(self, request):
        self.request = request

    @property
    def category_create_form(self):
        category_create_form = CategoryCreateForm(validator=partial(validate_unique_name, dbsession=self.request.dbsession)).bind(request=self.request)
        submit = deform.Button(name='Save', css_class='btn btn-info')
        cancel = deform.Button(name='Cancel', css_class='btn btn-inverse')
        return Form(category_create_form, buttons=(submit, cancel, ))

    @view_config(route_name='admin_categories', renderer='../templates/admin/categories/categories_list.jinja2', permission='user')
    def admin_categories(self):
        title = 'Categories list'
        page = int(self.request.params.get('page', 1))
        paginator = CategoryService.get_paginator(request=self.request, page=page)
        return {'title': title, 'paginator': paginator}

    @view_config(route_name='category_posts', renderer='../templates/admin/categories/category_posts_list.jinja2',
                 permission='user')
    def category_posts(self):
        slug = self.request.matchdict['slug']
        category = self.request.dbsession.query(Category).filter_by(slug=slug).one()
        posts = PostService.by_category(self.request, category=category.name)
        return {'posts': posts, 'category': category}

    @view_config(route_name='category_create', renderer='../templates/admin/categories/category_create.jinja2', permission='user')
    def category_create(self):
        title = 'Create a category'

        form = self.category_create_form

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

    @view_config(route_name='category_edit', renderer='../templates/admin/categories/category_edit.jinja2', permission='user')
    def category_edit(self):
        form = CategoryEditForm(self.request.POST)
        slug = self.request.matchdict['slug']
        category = self.request.dbsession.query(Category).filter_by(slug=slug).one()
        form.description.data = category.description

        if self.request.method == "POST" and form.validate():
            new_category_description = self.request.params.get('description')

            self.request.dbsession.query(Category).filter(Category.slug == slug)\
            .update({'description': new_category_description})

            url = self.request.route_url('admin_categories')
            return HTTPFound(location=url)

        return {'form': form, 'slug': slug, 'category': category}

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

    @view_config(route_name='user_posts', renderer='../templates/admin/users/user_posts_list.jinja2',
                 permission='admin')
    def user_posts(self):
        username = self.request.matchdict['username']
        posts = PostService.by_user(self.request, username=username)
        return {'posts': posts, 'username': username}

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
