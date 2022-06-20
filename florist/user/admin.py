# from flask_admin.contrib.mongoengine import ModelView
from ..admin.views import ModelView

from .models import User, Role

class UserModelView(ModelView):
    can_create = False

    column_exclude_list = ['password', 'fs_uniquifier']
    column_editable_list = ['active']
    column_searchable_list = ['email']
    column_filters = ['active']

    form_excluded_columns = ['password', 'fs_uniquifier', 'confirmed_at']
    
    def __init__(self, *a, **kw):
        super().__init__(User, *a, **kw)

def init(admin):
    admin.add_view(UserModelView())
    admin.add_view(ModelView(Role))
