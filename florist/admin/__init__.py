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
        # url 要从这里传入，可能是 flask-admin 的 bug。
        index_view = AdminIndexView(url=url)

    global admin
    # url 从这里传入不会改变，可能是 flask-admin 的 bug。
    admin = Admin(app, name=name, index_view=index_view, template_mode='bootstrap4')

    for pkg in app.config['FLORIST_ADMIN_PACKAGES']:
        import_module(f'{pkg}.admin')
    # 加载 user.admin
    import_module('florist.user.admin')