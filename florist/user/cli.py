import click
import logging
from uuid import uuid4
from mongoengine import errors
from flask_security.utils import hash_password
from flask_security.cli import users


@users.command('createsuperuser')
@click.argument('name')
@click.password_option()
@click.argument('mobile')
@click.argument('email')
def createsuperuser(name, password, mobile, email):
    from .models import user_datastore
    admin_role = user_datastore.find_or_create_role(
        user_datastore.role_model.admin_name
    )
    try:
        user_datastore.create_user(
            username=name,
            us_phone_number=mobile,
            email=email,
            password=hash_password(password),
            roles=[admin_role],
            fs_uniquifier=uuid4().hex + uuid4().hex,  # 64 字符。
        )
    except errors.MongoEngineException:
        logging.exception('创建超级用户失败。')


@users.command(
    'all',
    short_help=("List all users."),
)
def all():
    from .models import user_datastore
    users = user_datastore.user_model.objects.all()
    for u in users:
        print(u.username or u.email)
