import pathlib
import hashlib
import mongoengine.errors
from flask import Blueprint, render_template, flash, g, request, current_app, abort, redirect, url_for

template_folder = pathlib.Path(__file__).parent / 'templates'

admin_bp = Blueprint('admin', __name__, template_folder=template_folder)


def hash_password(pwd):
    if isinstance(pwd, str):
        pwd = pwd.encode()
    return hashlib.sha256(pwd).hexdigest()


from ...db import db

class User(db.Document):
    username = db.StringField(max_length=50, unique=True, required=True)
    hashed_password =db.StringField(required=True)
    is_staff = db.BooleanField(default=False)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)


@admin_bp.route("/")
def signin():
    return render_template('signin.html')


@admin_bp.post("/register/")
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    current_app.logger.debug(f'{request.form=}, {username=}, {password=}')
    user = User(username=username, hashed_password=hash_password(password))
    try:
        user.save()
    except mongoengine.errors.MongoEngineException as e:
        flash(f"注册失败。错误：{e}", category="alert")
    else:
        flash("注册成功。", category="success")

    return redirect(url_for('.signin'))


@admin_bp.post("/auth/")
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    # current_app.logger.debug(f'{request.form=}, {username=}, {password=}')
    try:
        g.user = User.objects.get(username=username, hashed_password=hash_password(password))
    except mongoengine.errors.DoesNotExist:
        flash("用户不存在，或密码错误。", category="failed")
        return redirect(url_for('.signin'))
    current_app.logger.debug(f"before {g.user=}")
    return redirect(url_for('.dashboard'))

@admin_bp.get("/signout/")
def signout():
    g.user = None
    flash('退出成功。')
    return redirect(url_for('.signin'))


@admin_bp.get("/dashboard/")
def dashboard():
    return "<h1>Dashboard.</h1>"
