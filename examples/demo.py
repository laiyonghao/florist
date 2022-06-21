
from flask import Flask

app = Flask(__name__)
app.config.from_object('florist.settings')
app.config.from_object('settings')

from florist import init
init(app)

# 业务网站
from florist.cms import cms_bp
app.register_blueprint(cms_bp, url_prefix='/')
