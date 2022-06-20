from flask import Blueprint

site_bp = Blueprint('site', __name__)

from ..cms import cms_bp
site_bp.register_blueprint(cms_bp)
# from ..contrib.admin import admin_bp
# site_bp.register_blueprint(admin_bp, url_prefix='/admin')

def init(app):
    from ..user import init as user_init
    user_init(app)
    
    from .admin import init as admin_init
    admin_init(app, url_prefix='/admin')

    app.register_blueprint(site_bp, url_prefix='/')
