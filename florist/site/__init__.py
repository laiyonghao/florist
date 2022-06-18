from flask import Blueprint
from ..contrib.admin import admin_bp
from ..contrib.cms import cms_bp

site_bp = Blueprint('site', __name__)

site_bp.register_blueprint(cms_bp)
site_bp.register_blueprint(admin_bp, url_prefix='/admin')
