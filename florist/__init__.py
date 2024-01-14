from functools import cache

cache = None  # noqa


def init(app, *a, **kw):
    global cache
    # 初始化缓存
    from flask_caching import Cache
    cache = Cache(app)
    # 初始化数据库
    from .db import init as db_init
    db_init(app)
    # 初始化用户
    from .user import init as user_init
    user_init(app)
    # 初始化管理后台
    from .admin import init as admin_init
    admin_init(app, *a, **kw)
