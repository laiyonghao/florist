from functools import partial
from mongoengine import fields

from ...db import db
from ...user.models import User

class EventLog(db.Document):
    occurred_at = fields.DateTimeField(required=True)
    subject = fields.ReferenceField(User, required=True)
    predicate = fields.StringField(min_length=1, required=True)
    object = fields.GenericReferenceField(required=True)
    ext_info = fields.DictField()

    meta = {
        'indexes': [
            ('predicate', 'subject'),
            ('predicate', 'object'),
            ('predicate', 'occurred_at'),
            ('subject', 'occurred_at'),
            ('object', 'occurred_at'),
        ]
    }

    # @classmethod
    # def add(cls, *a, **kw):
    #     obj = cls(*a, **kw)
    #     obj.save()
    #     return obj

    # @classmethod
    # def __getattribute__(cls, attr: str):
    #     try:
    #         return super().__getattribute__(attr)
    #     except AttributeError as e:
    #         if attr.startswith('add_'):
    #             return partial(cls.add, predicate=attr.removeprefix('add_'))
    #         raise e
