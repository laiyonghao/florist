from flask_ckeditor import CKEditor, CKEditorField
from ...admin import admin, ModelView
from .models import Article
from flask_admin.contrib.fileadmin import FileAdmin

class ArticleView(ModelView):
    model_class = Article

    column_exclude_list = ['content_type', 'content']
    form_excluded_columns = ['content_type', 'published_at', 'updated_at']
    form_overrides = dict(content=CKEditorField)

    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

admin.add_view(ArticleView())
