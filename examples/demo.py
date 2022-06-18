from florist.site import site_bp

# site = Site(__name__)

# @site.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

from flask import Flask

app = Flask(__name__)
app.register_blueprint(site_bp)