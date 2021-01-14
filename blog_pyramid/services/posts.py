import paginate_sqlalchemy

from blog_pyramid.models.post import Post


class PostService:

    @classmethod
    def all(cls, request):
        return request.dbsession.query(Post).order_by(Post.created.desc())

    @classmethod
    def get_paginator(cls, request, page=1):
        if request.user.role == 'admin':
            query = request.dbsession.query(Post).order_by(Post.created.desc())
        else:
            query = request.dbsession.query(Post).filter(Post.author == request.user.username).order_by(Post.created.desc())
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return paginate_sqlalchemy.SqlalchemyOrmPage(query, page, items_per_page=3, url_maker=url_maker)

    @classmethod
    def by_user(cls, request, username):
        return request.dbsession.query(Post).filter(Post.author == username).order_by(Post.created.desc())

    @classmethod
    def by_category(cls, request, category):
        if request.user.role == 'admin':
            return request.dbsession.query(Post).filter(Post.category == category).order_by(Post.created.desc())
        else:
            return request.dbsession.query(Post).filter(Post.category == category, Post.author == request.user.username).\
                order_by(Post.created.desc())


class PostServiceBlog:

    @classmethod
    def all(cls, request, page=1):
        query = request.dbsession.query(Post).order_by(Post.created.desc())
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return paginate_sqlalchemy.SqlalchemyOrmPage(query, page, items_per_page=3, url_maker=url_maker)

    @classmethod
    def by_category(cls, request, category, page=1):
        query = request.dbsession.query(Post).filter(Post.category == category).order_by(Post.created.desc())
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return paginate_sqlalchemy.SqlalchemyOrmPage(query, page, items_per_page=3, url_maker=url_maker)

    @classmethod
    def by_user(cls, request, username, page=1):
        query = request.dbsession.query(Post).filter(Post.author == username).order_by(Post.created.desc())
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return paginate_sqlalchemy.SqlalchemyOrmPage(query, page, items_per_page=3, url_maker=url_maker)