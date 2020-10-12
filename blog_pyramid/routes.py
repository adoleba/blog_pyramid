def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('admin', '/admin')
    config.add_route('admin_posts', '/admin/posts')
    config.add_route('post_create', '/admin/posts/create')
    config.add_route('admin_categories', '/admin/categories')
