# from flask import Blueprint

# site_bp = Blueprint('site', __name__)

def init(app, *a, **kw):
    # 初始化数据库
    from .db import init as db_init
    db_init(app)
    # 初始化用户
    from .user import init as user_init
    user_init(app)

    # from ..contrib.admin import admin_bp
    # site_bp.register_blueprint(admin_bp, url_prefix='/admin')
    # 初始化管理后台
    from .admin import init as admin_init
    admin_init(app, *a, **kw)
    # 初始化前台
    # from ..cms import cms_bp
    # site_bp.register_blueprint(cms_bp)
    # # 挂载到app
    # app.register_blueprint(site_bp, url_prefix='/')

    # class A(object):
    #     def __init__(self) -> None:
    #         self.object = 'ccc'
    # a = A()
    # print(a.object)
