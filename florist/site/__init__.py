from flask import Blueprint

site_bp = Blueprint('site', __name__)

from ..cms import cms_bp
site_bp.register_blueprint(cms_bp)
# from ..contrib.admin import admin_bp
# site_bp.register_blueprint(admin_bp, url_prefix='/admin')

def init(app):
    app.register_blueprint(site_bp, url_prefix='/')

    from .admin import init as admin_init
    admin_init(app, url_prefix='/admin')
    
    from flask_security import Security
    from ..user.models import user_datastore
    security = Security(app, user_datastore)
