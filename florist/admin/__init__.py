import pathlib
from importlib import import_module
from flask import Blueprint
from flask_admin import Admin
from .views import AdminIndexView, ModelView # noqa
from .form.fields import ImageInputWidgetExtraJs  # noqa

admin = None

static_folder = pathlib.Path(__file__).parent / 'static'
florist_bp = Blueprint('florist_bp', __name__, static_folder=static_folder)


@florist_bp.route('/static/js/image_input_widget.js')
def image_input_widget_js():
    return florist_bp.send_static_file('js/image_input_widget.js')


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
    admin = Admin(
        app, name=name, index_view=index_view, template_mode='bootstrap4')

    if app.config.get('FLORIST_REDISCLI_ENBLED'):
        from flask_admin.contrib import rediscli
        from redis import Redis
        admin.add_view(rediscli.RedisCli(Redis(), category='系统'))

    app.register_blueprint(florist_bp, url_prefix=f'{admin.url}/florist')

    for pkg in app.config['FLORIST_ADMIN_PACKAGES']:
        import_module(f'{pkg}.admin')
    # 加载 user.admin
    import_module('florist.user.admin')
