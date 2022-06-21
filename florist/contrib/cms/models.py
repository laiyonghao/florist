from ...db import db

class Article(db.Document):
    title = db.StringField(max_length=255)
    content = db.StringField()
    published_at = db.DateTimeField()
