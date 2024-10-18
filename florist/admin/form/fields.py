from wtforms import StringField

from .widgets import ImageInputWidget


class ImageField(StringField):
    widget = ImageInputWidget()
