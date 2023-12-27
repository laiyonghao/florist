import pathlib
from flask import Blueprint

template_folder = pathlib.Path(__file__).parent / 'templates'
cms_bp = Blueprint('cms', __name__, template_folder=template_folder)


@cms_bp.route("/")
def hello_world():
    return "<p>Hello, CMS!</p>"