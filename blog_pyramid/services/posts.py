from blog_pyramid.models.post import Post
import paginate_sqlalchemy


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
