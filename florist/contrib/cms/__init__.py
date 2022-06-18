from flask import Blueprint

cms_bp = Blueprint('cms', __name__)

@cms_bp.route("/")
def hello_world():
    return "<p>Hello, CMS!</p>"