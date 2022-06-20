from flask_admin import Admin

def init(app, url_prefix=None, name=None):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    if not url_prefix:
        url_prefix = '/admin'
    if not name:
        name = 'Florist Admin'

    admin = Admin(app, url=url_prefix, name=name, template_mode='bootstrap4')

    from ..user.admin import init as user_admin_init
    user_admin_init(admin)