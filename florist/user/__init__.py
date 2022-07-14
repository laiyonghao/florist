security = None
def init(app):
    global security

    # ensure admin
    # from .models import Role, User
    # @app.before_first_request
    # def ensure_admin():
    #     admin_role = Role.ensure_admin()
    #     User.ensure_admin(app.config, admin_role)

    from flask_security import Security
    from .models import user_datastore
    from .forms import ExtendedRegisterForm
    security = Security(
        app=app,
        datastore=user_datastore,
        register_form=ExtendedRegisterForm,
    )

    from .cli import init as cli_init
    cli_init(app)