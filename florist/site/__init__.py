from flask import Blueprint

site_bp = Blueprint('site', __name__)

# site = app = Flask(__name__)
@site_bp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"