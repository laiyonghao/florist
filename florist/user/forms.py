from flask_security.forms import RegisterForm, Required
from wtforms import StringField

class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])
    mobile = StringField('Mobile', [Required()])
    nickname = StringField('Nickname', [Required()])