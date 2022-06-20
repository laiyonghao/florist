
from flask import Flask

app = Flask(__name__)
app.secret_key = "florist demo site secret key"
app.config['MONGODB_SETTINGS'] = {'DB': 'florist-demo'}

from florist.db import init as db_init
db_init(app)

from florist.site import init as site_init
site_init(app)
