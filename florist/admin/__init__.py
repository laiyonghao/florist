from importlib import import_module
from flask_admin import Admin
from .views import AdminIndexView, ModelView

admin = None

def init(app, url_prefix=None, name=None, index_view=None):
    if not url_prefix:
        url_prefix = '/admin'
    if not name:
        name = 'Florist Admin'
    if not index_view:
        index_view = AdminIndexView()

    global admin
    admin = Admin(app, url=url_prefix, name=name, index_view=index_view, template_mode='bootstrap4')
    # 加载 user.admin
    import_module('florist.user.admin')
