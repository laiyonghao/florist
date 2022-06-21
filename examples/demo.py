
from flask import Flask

app = Flask(__name__)
# 先加载库配置
app.config.from_object('florist.settings')
# 后加载项目配置
app.config.from_object('settings')

from florist import init
init(app)

# 业务网站
from florist.contrib.cms import cms_bp
app.register_blueprint(cms_bp, url_prefix='/')
