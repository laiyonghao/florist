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

        import redis

        redis_url = app.config.get(
            'FLORIST_REDIS_URL',
            'redis://localhost:6379/0',
        )
        try:
            rediscli_client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
                encoding_errors='backslashreplace',
            )
        except TypeError:
            rediscli_client = redis.Redis.from_url(
                redis_url,
                decode_responses=True,
            )

        # Flask-Admin 的 RedisCli 不读取 Flask 配置；它只接受一个 Redis 连接对象。
        # redis_client 由 florist.init() 统一创建。
        admin.add_view(rediscli.RedisCli(rediscli_client, category='系统'))

    app.register_blueprint(florist_bp, url_prefix=f'{admin.url}/florist')

    for pkg in app.config['FLORIST_ADMIN_PACKAGES']:
        import_module(f'{pkg}.admin')
    # 加载 user.admin
    import_module('florist.user.admin')
