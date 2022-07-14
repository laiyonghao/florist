from importlib import import_module
from flask_admin import Admin
from .views import AdminIndexView, ModelView # noqa

admin = None

def init(app, url=None, name=None, index_view=None):
    if not url:
        url = app.config['FLORIST_ADMIN_URL']
    if not name:
        name = app.config['FLORIST_ADMIN_SITE_NAME']
    if not index_view:
        index_view = AdminIndexView()

    global admin
    admin = Admin(app, url=url, name=name, index_view=index_view, template_mode='bootstrap4')

    for pkg in app.config['FLORIST_ADMIN_PACKAGES']:
        import_module(f'{pkg}.admin')
    # 加载 user.admin
    import_module('florist.user.admin')