from flask_security import (
    uia_phone_mapper,
    uia_email_mapper,
    uia_username_mapper,
)

# ------ Flask-Admin ------
FLASK_ADMIN_SWATCH = 'cerulean'
# ------ Flask-Admin ------

# ------ Flask-Security ------
SECURITY_URL_PREFIX = '/users'
# SECURITY_REGISTERABLE = True
# SECURITY_RECOVERABLE = True
# SECURITY_TOTP_SECRETS = {
#     "1": "BSBMWGvOMbOrLwe6PzMkUYR8cXDdBCm7LOLezsnKbYv"
# }
SECURITY_US_ENABLED_METHODS = ["password", "sms"]
SECURITY_UNIFIED_SIGNIN = True
SECURITY_USERNAME_ENABLE = True
SECURITY_PHONE_REGION_DEFAULT = 'CN'
SECURITY_USER_IDENTITY_ATTRIBUTES = [
    {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
    {"us_phone_number": {"mapper": uia_phone_mapper}},
    {"username": {"mapper": uia_username_mapper}},
]
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
FLORIST_ADMIN_URL = '/admin'
FLORIST_ADMIN_SITE_NAME = 'Florist Admin'
FLORIST_ADMIN_PACKAGES = ()
# ------ Florist ------
