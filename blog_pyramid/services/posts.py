from blog_pyramid.models.post import Post


class PostService:

    @classmethod
    def all(cls, request):
        query = request.dbsession.query(Post)
        return query.order_by(-Post.created)
