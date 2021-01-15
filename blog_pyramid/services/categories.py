import paginate_sqlalchemy

from blog_pyramid.models.category import Category


class CategoryService:

    @classmethod
    def all(cls, request, page=1):
        query = request.dbsession.query(Category).order_by(Category.name)
        query_params = request.GET.mixed()

        def url_maker(link_page):
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return paginate_sqlalchemy.SqlalchemyOrmPage(query, page, items_per_page=2, url_maker=url_maker)


class CategoryBlogService:
    @classmethod
    def all(cls, request):
        query = request.dbsession.query(Category)
        return query.order_by(Category.name)
