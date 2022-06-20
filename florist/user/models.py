from flask_security import MongoEngineUserDatastore, UserMixin, RoleMixin
    
from ..db import db

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    username = db.StringField(max_length=255, unique=True)
    nickname = db.StringField(max_length=255)
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    # is_staff = db.BooleanField(default=False)
    fs_uniquifier = db.StringField(max_length=64, unique=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
