from florist.site import site_bp

from flask import Flask

app = Flask(__name__)
app.register_blueprint(site_bp)