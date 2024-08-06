from flask_security import Security
from .models import user_datastore
from .forms import ExtendedRegisterForm
security = Security(
    datastore=user_datastore,
    register_form=ExtendedRegisterForm,
)


def init(app):
    global security
    security.init_app(app)
    from . import cli
