from functools import partial
from mongoengine import fields

from ...db import db
# from ...user.models import User

class File(db.Document):
    file = fields.FileField()
    # occurred_at = fields.DateTimeField(required=True)
    # subject = fields.ReferenceField(User, required=True)
    # predicate = fields.StringField(min_length=1, required=True)
    # object = fields.GenericReferenceField(required=True)
    # ext_info = fields.DictField()


    meta = {
        'indexes': [
            # ('predicate', 'subject'),
            # ('predicate', 'object'),
            # ('predicate', 'occurred_at'),
            # ('subject', 'occurred_at'),
            # ('object', 'occurred_at'),
        ]
    }