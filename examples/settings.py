# ------ Flask ------
SECRET_KEY = "florist demo site secret key"
# ------ Flask ------

# ------ Flask-Mongoengine ------
MONGODB_SETTINGS = {'DB': 'florist-demo'}
# ------ Flask-Mongoengine ------

# ------ Flask-Security ------
SECURITY_PASSWORD_SALT = 'a58063c79d92865d79'
SECURITY_TOTP_SECRETS = {
    "1": "BSBMWGvOMbOrLwe6PzMkUYR8cXDdBCm7LOLezsnKbYv"
}
# ------ Flask-Security ------

# ------ Flask-thumbnails ------

# ------ Flask-thumbnails ------

# ------ Florist ------
FLORIST_ADMIN_PACKAGES = (
    'florist.contrib.event',
    'florist.contrib.meterial',
    'florist.contrib.cms',
)
# ------ Florist ------

FLASKFILEMANAGER_FILE_PATH = UPLOADED_PATH = './static/'

from dev_settings import *