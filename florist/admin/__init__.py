from importlib import import_module
from flask_admin import Admin
from .views import AdminIndexView, ModelView
from flask_ckeditor import CKEditor
from flask_admin.contrib.fileadmin import FileAdmin as OrigFileAdmin
# import os.path as op
from flask_admin.babel import gettext, lazy_gettext

admin = None

class FileAdmin(OrigFileAdmin):
    # Modals
    rename_modal = True
    """Setting this to true will display the rename view as a modal dialog."""

    upload_modal = True
    """Setting this to true will display the upload view as a modal dialog."""

    mkdir_modal = True
    """Setting this to true will display the mkdir view as a modal dialog."""

    edit_modal = True
    """Setting this to true will display the edit view as a modal dialog."""
    # editable_extensions = ('md', 'html', 'txt')

    def _save_form_files(self, directory, path, form):
        filename = self._separator.join([directory, form.upload.data.filename])

        if self.storage.path_exists(filename):
            secure_name = self._separator.join([path, form.upload.data.filename])
            raise Exception(gettext('File "%(name)s" already exists.',
                                    name=secure_name))
        else:
            self.save_file(filename, form.upload.data)
            self.on_file_upload(directory, path, filename)


def init(app, url_prefix=None, name=None, index_view=None):
    if not url_prefix:
        url_prefix = '/admin'
    if not name:
        name = 'Florist Admin'
    if not index_view:
        index_view = AdminIndexView()

    global admin
    admin = Admin(app, url=url_prefix, name=name, index_view=index_view, template_mode='bootstrap4')
    admin.add_view(FileAdmin('static/', '/static/', name='Static Files'))

    ckeditor = CKEditor(app)

    for pkg in app.config['FLORIST_ADMIN_PACKAGES']:
        import_module(f'{pkg}.admin')
    # 加载 user.admin
    import_module('florist.user.admin')


# 加个引用，让 linter 开心。
ModelView