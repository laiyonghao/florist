from mongoengine import fields
from datetime import datetime
from enum import Enum

from ...db import db


class ContentTyep(Enum):
    RichText = 'rt'
    Markdown = 'md'


class Article(db.Document):
    title = fields.StringField(max_length=255)
    content = fields.StringField()
    content_type = fields.EnumField(ContentTyep, default=ContentTyep.RichText)
    published_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(null=True)

    def save(self,
             force_insert=False,
             validate=True,
             clean=True,
             write_concern=None,
             cascade=None,
             cascade_kwargs=None,
             _refs=None,
             save_condition=None,
             signal_kwargs=None,
             **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(force_insert, validate, clean, write_concern,
                            cascade, cascade_kwargs, _refs, save_condition,
                            signal_kwargs, **kwargs)
