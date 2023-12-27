security = None


def init(app):
    global security

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