import mongoengine.errors
from flask_security import MongoEngineUserDatastore, UserMixin, RoleMixin

from florist.contrib.admin import hash_password

from ..db import db

class Role(db.Document, RoleMixin):
    admin_name = 'admin'

    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def ensure_admin(cls):
        try:
            return cls.objects.get(name=cls.admin_name)
        except mongoengine.errors.DoesNotExist:
            role = cls(name=cls.admin_name, description='超管')
            role.save()
            return role

    def delete(self, signal_kwargs=None, **write_concern):
        if self.name == self.admin_name:
            raise RuntimeError("Can't delete `admin` role.")
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

    @classmethod
    def ensure_admin(cls, config, admin_role):
        admin_username = config.get('FLORIST_ADMIN_USERNAME', 'admin')
        admin_mobile = config.get('FLORIST_ADMIN_MOBILE', '13800123123')
        admin_email = config.get('FLORIST_ADMIN_EMAIL', 'admin@example.com')
        admin_password = config.get('FLORIST_ADMIN_PASSWORD', 'nimda321')
        try:
            user = cls(username=admin_username, mobile=admin_mobile, email=admin_email, password=hash_password(admin_password), roles=[admin_role])
            user.save()
        except mongoengine.errors.MongoEngineException:
            pass
        
    def __str__(self):
        return self.nickname or self.username


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)

