import pathlib
from flask import Blueprint, render_template, flash, g, request, current_app, abort, redirect, url_for

template_folder = pathlib.Path(__file__).parent / 'templates'

admin_bp = Blueprint('admin', __name__, template_folder=template_folder)



@admin_bp.route("/")
def signin():
    print(url_for('site.admin.signin'))
    print('#'*80)
    return render_template('signin.html')

@admin_bp.post("/cup/")
def check_username_password():
    # g.user = None
    # flash('退出成功。')
    username = request.form.get('username')
    password = request.form.get('password')
    current_app.logger.debug(f'{request.form=}, {username=}, {password=}')
    # return render_template('signin.html')
    flash("尝试登陆")
    return redirect(url_for('.signin'))


@admin_bp.get("/signout/")
def signout():
    g.user = None
    flash('退出成功。')
    return render_template('signin.html')


