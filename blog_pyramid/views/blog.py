from pyramid.view import view_config


@view_config(route_name='index', renderer='../templates/blog/posts.jinja2', permission='view')
def index(request):
    title = 'Welcome to my blog'
    return {'title': title}
