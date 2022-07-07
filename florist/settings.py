# ------ Flask-Admin ------
FLASK_ADMIN_SWATCH = 'cerulean'
# ------ Flask-Admin ------

# ------ Flask-Security ------
SECURITY_URL_PREFIX = '/users'
# SECURITY_REGISTERABLE = True
# SECURITY_RECOVERABLE = True
SECURITY_USER_IDENTITY_ATTRIBUTES = ['username', 'email', 'mobile']
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
# ------ Flask-Security ------

CKEDITOR_FILE_BROWSER = 'flaskfilemanager.index'
CKEDITOR_FILE_UPLOADER = 'meterialadmin.ckeditor_upload'
CKEDITOR_HEIGHT = 500
CKEDITOR_SERVE_LOCAL = True

# ------ Florist ------
FLORIST_ADMIN_USERNAME = 'admin'
FLORIST_ADMIN_MOBILE = '13000000000'
FLORIST_ADMIN_EMAIL ='admin@example.com'
FLORIST_ADMIN_PASSWORD = 'nimda321'

FLORIST_ADMIN_PACKAGES = ()
# ------ Florist ------
