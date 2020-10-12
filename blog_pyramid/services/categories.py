from blog_pyramid.models.category import Category


class CategoryService:

    @classmethod
    def all(cls, request):
        query = request.dbsession.query(Category)
        return query.order_by(Category.name)
