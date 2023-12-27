from ..admin import admin, ModelView

from .models import User, Role


class UserModelView(ModelView):
    model_class = User

    can_create = False

    column_exclude_list = ['password', 'fs_uniquifier']
    column_editable_list = ['active']
    column_searchable_list = ['email', 'username', 'nickname']
    column_filters = ['active']

    form_excluded_columns = ['password', 'fs_uniquifier', 'confirmed_at']


admin.add_view(UserModelView())
admin.add_view(ModelView(Role))
