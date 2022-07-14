import mongoengine.errors
from flask_security import MongoEngineUserDatastore, UserMixin, RoleMixin
from flask_security.utils import hash_password

from ..db import db

class Role(db.Document, RoleMixin):
    admin_name = 'admin'

    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)

    def __str__(self):
        return self.name

    def delete(self, signal_kwargs=None, **write_concern):
        if self.name == self.admin_name:
            raise RuntimeError(f"Can't delete `{self.admin_name}` role.")
        return super().delete(signal_kwargs, **write_concern)

class User(db.Document, UserMixin):
    username = db.StringField(max_length=255, unique=True)
    nickname = db.StringField(max_length=255)
    mobile = db.StringField(max_length=255, unique=True)
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    # is_staff = db.BooleanField(default=False)
    fs_uniquifier = db.StringField(max_length=64, unique=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def __str__(self):
        return self.nickname or self.username


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)

