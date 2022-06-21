from flask_admin import Admin
from .views import AdminIndexView

def init(app, url_prefix=None, name=None, index_view=None):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    if not url_prefix:
        url_prefix = '/admin'
    if not name:
        name = 'Florist Admin'
    if not index_view:
        index_view = AdminIndexView()

    admin = Admin(app, url=url_prefix, name=name, index_view=index_view, template_mode='bootstrap4')

    # 此处应改为服务发现。
    from ..user.admin import init as user_admin_init
    user_admin_init(admin)
