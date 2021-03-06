def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # admin - main
    config.add_route('admin', '/admin')
    config.add_route('login', '/admin/login')
    config.add_route('logout', '/admin/logout')
    config.add_route('admin_posts', '/admin/posts')
    config.add_route('admin_own_posts', '/admin/{username}/posts')
    config.add_route('admin_categories', '/admin/categories')
    config.add_route('admin_users', '/admin/users')

    # categories
    config.add_route('category_create', '/admin/categories/create')
    config.add_route('category_edit', '/admin/categories/{slug}/edit')
    config.add_route('category_delete', '/admin/categories/{slug}/delete')
    config.add_route('category_posts', '/admin/categories/{slug}/posts')
    config.add_route('category_delete_confirmed', '/admin/categories/{slug}/delete/confirmed')

    # posts
    config.add_route('post_create', '/admin/posts/create')
    config.add_route('post_edit', '/admin/posts/{slug}/edit')
    config.add_route('post_delete', '/admin/posts/{slug}/delete')
    config.add_route('post_delete_confirmed', '/admin/posts/{slug}/delete/confirmed')

    # users
    config.add_route('user_register', '/admin/users/register')
    config.add_route('user_edit', '/admin/users/{username}/edit')
    config.add_route('user_email_edit', '/admin/users/{username}/email_edit')
    config.add_route('user_password_edit', '/admin/users/{username}/password_edit')
    config.add_route('user_posts', '/admin/users/{username}/posts')
    config.add_route('user_profile', '/admin/users/{username}/profile')

    #blog
    config.add_route('index', '/')
    config.add_route('post_page', '/{slug}')
    config.add_route('blog_category_posts', 'posts/category/{category_slug}')
    config.add_route('blog_user_posts', 'posts/user/{username}')
