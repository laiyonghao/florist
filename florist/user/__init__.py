security = None
def init(app):
    global security

    # ensure admin
    from .models import Role, User
    @app.before_first_request
    def ensure_admin():
        admin_role = Role.ensure_admin()
        User.ensure_admin(app.config, admin_role)

    app.config['SECURITY_URL_PREFIX'] = '/users'
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_RECOVERABLE'] = True
    app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ['username', 'email', 'mobile']
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
    app.config['SECURITY_SEND_PASSWORD_RESET_EMAIL'] = False
    app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False
    app.config['SECURITY_PASSWORD_SALT'] = 'a58063c79d92865d79'


    from flask_security import Security
    from .models import user_datastore
    from .forms import ExtendedRegisterForm
    security = Security(
        app=app,
        datastore=user_datastore,
        register_form=ExtendedRegisterForm,
    )
