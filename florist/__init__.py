cache = None  # noqa
limiter = None  # noqa


def init(app, *a, **kw):
    global cache, limiter
    # 初始化缓存
    from flask_caching import Cache
    cache = Cache(app)
    # 初始化数据库
    from .db import init as db_init
    db_init(app)
    # 初始化限流器
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    limiter = Limiter(
        get_remote_address,
        app=app,
        # default_limits=["10/s",],  # 一个IP最多请求10次
        # storage_uri="memory://",
        storage_uri="redis://localhost:6379",
    )
    # 初始化用户
    from .user import init as user_init
    user_init(app)
    # 初始化管理后台
    from .admin import init as admin_init
    admin_init(app, *a, **kw)
