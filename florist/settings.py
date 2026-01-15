from flask_security import (
    uia_phone_mapper,
    uia_email_mapper,
    uia_username_mapper,
)

SEND_FILE_MAX_AGE_DEFAULT = 60*60*24

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
SECURITY_US_ENABLED_METHODS = ["password",]
SECURITY_UNIFIED_SIGNIN = True
SECURITY_USERNAME_ENABLE = True
SECURITY_PHONE_REGION_DEFAULT = 'CN'
SECURITY_USER_IDENTITY_ATTRIBUTES = [
    {"email": {"mapper": uia_email_mapper, "case_insensitive": True}},
    {"username": {"mapper": uia_username_mapper}},
    {"us_phone_number": {"mapper": uia_phone_mapper}},
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
FLORIST_REDISCLI_ENBLED = False
# ------ Florist ------

# ------ Florist Thumbs (Jinja filter: thumb) ------
# Enable/disable thumbs feature globally.
FLORIST_THUMBS_ENABLED = True

# URL prefix for serving generated thumbs via Flask (dev-friendly).
# In production you can serve FLORIST_THUMBS_CACHE_DIR via nginx/CDN
# and keep this route.
FLORIST_THUMBS_URL_PREFIX = '/thumbs'

# Where to store generated thumbs.
# If not set, defaults to UPLOADED_PATH / FLORIST_THUMBS_CACHE_SUBDIR.
FLORIST_THUMBS_CACHE_DIR = None
FLORIST_THUMBS_CACHE_SUBDIR = '_thumbs'

# Only allow explicitly whitelisted output formats.
FLORIST_THUMBS_ALLOWED_FORMATS = ('jpg', 'png', 'webp')

# Defaults and safety limits.
FLORIST_THUMBS_DEFAULT_QUALITY = 70
FLORIST_THUMBS_MAX_SCALE_UP = 2.0
FLORIST_THUMBS_MAX_DIMENSION = 8192

# Mapping: URL prefix -> filesystem subdir
# (relative to UPLOADED_PATH) or absolute dir.
# Example: {"/wx/avatars/": "avatars", "/meterial/": ""}
FLORIST_THUMBS_SOURCE_PREFIXES = {}
# ------ Florist Thumbs ------
