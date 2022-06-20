from flask_mongoengine import MongoEngine

db = MongoEngine()

def init(app):
    db.init_app(app)
