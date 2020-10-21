def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('admin', '/admin')
    config.add_route('admin_posts', '/admin/posts')
    config.add_route('admin_categories', '/admin/categories')
    config.add_route('admin_users', '/admin/users')
    config.add_route('category_create', '/admin/categories/create')
    config.add_route('category_edit', '/admin/categories/{slug}/edit')
    config.add_route('category_delete', '/admin/categories/{slug}/delete')
    config.add_route('category_delete_confirmed', '/admin/categories/{slug}/delete/confirmed')
    config.add_route('post_create', '/admin/posts/create')
    config.add_route('post_edit', '/admin/posts/{slug}/edit')
    config.add_route('post_delete', '/admin/posts/{slug}/delete')
    config.add_route('post_delete_confirmed', '/admin/posts/{slug}/delete/confirmed')
    config.add_route('user_register', '/admin/users/register')
    config.add_route('user_edit', '/admin/users/{username}/edit')
    config.add_route('user_email_edit', '/admin/users/{username}/email_edit')
