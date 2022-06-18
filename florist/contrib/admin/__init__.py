import pathlib
from flask import Blueprint, render_template

template_folder = pathlib.Path(__file__).parent / 'templates'

admin_bp = Blueprint('admin', __name__, template_folder=template_folder)

@admin_bp.route("/")
def hello_world():
    # return "<p>Hello, Admin!</p>"
    return render_template('login.html')
