from florist.site import site_bp

from flask import Flask

app = Flask(__name__)
app.secret_key = "florist demo site secret key"

app.register_blueprint(site_bp)


# 借鉴 flask-admin
from flask_admin import Admin
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, url='/admin2', name='microblog', template_mode='bootstrap3')
# Add administrative views here