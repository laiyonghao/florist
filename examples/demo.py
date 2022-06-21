
from flask import Flask

app = Flask(__name__)
app.secret_key = "florist demo site secret key"
app.config['MONGODB_SETTINGS'] = {'DB': 'florist-demo'}


from florist.site import init as site_init
site_init(app)

# 业务网站
from florist.cms import cms_bp
app.register_blueprint(cms_bp, url_prefix='/')
