import hashlib, pathlib, os
from flask import Blueprint, send_from_directory, request, current_app, url_for
from flask_admin.babel import gettext, lazy_gettext
from flaskfilemanager import init as flaskfilemanager_init
from flask_admin.contrib.fileadmin import FileAdmin as OrigFileAdmin
from flask_ckeditor import upload_fail, upload_success
from ...admin import admin
from ...admin.views import is_accessible

static_folder = pathlib.Path(__file__).parent / 'static'
template_folder = pathlib.Path(__file__).parent / 'templates'
meterial_bp = Blueprint('meterialadmin', __name__, template_folder=template_folder)

def hash_filename(s):
    if isinstance(s, str):
        s = s.encode()
    return hashlib.sha256(s).hexdigest()

@meterial_bp.route('/meterial/ckeditor_upload/', methods=['POST'])
def ckeditor_upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)


@admin.app.route('/meterial/<filename>')
def uploaded_files(filename):
    path = admin.app.config['UPLOADED_PATH']
    return send_from_directory(path, filename)


class FileAdmin(OrigFileAdmin):
    # modal 功能有 bug，在抛异常时会跳转到单独的新页面，所以不使用。
    
    def _save_form_files(self, directory, path, form):
        fn =  f'{hash_filename(form.upload.data.filename)}.{form.upload.data.filename.rsplit(".")[-1]}'
        filename = self._separator.join([directory, fn])

        if self.storage.path_exists(filename):
            secure_name = self._separator.join([path, form.upload.data.filename])
            raise Exception(gettext('File "%(name)s" already exists.',
                                    name=secure_name))
        else:
            self.save_file(filename, form.upload.data)
            self.on_file_upload(directory, path, filename)


admin.add_view(FileAdmin('uploaded/', '/uploaded/', name='Uploaded Files'))
# 通过自定义回调实现相对路径。
# REF: https://github.com/psolom/RichFilemanager/issues/222
flaskfilemanager_init(
    admin.app,
    access_control_function=is_accessible,
    custom_init_js_path=static_folder / 'filemanager.init.js'
)
# https://github.com/psolom/RichFilemanager/wiki/How-to-open-the-Filemanager-from-CKEditor-in-a-modal-window
admin.app.register_blueprint(meterial_bp, url_prefix=f'{admin.url}/meterial')
