from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView

# from florist.contrib.admin import User
from ..user.models import User, Role

class UserModelView(ModelView):
    can_create = False

    column_exclude_list = ['password', 'fs_uniquifier']
    column_editable_list = ['active']
    column_searchable_list = ['email']
    column_filters = ['active']

    form_excluded_columns = ['password', 'fs_uniquifier', 'confirmed_at']
    
    def __init__(self, *a, **kw):
        super().__init__(User, *a, **kw)

def init(app, url_prefix):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, url=url_prefix, name='Florist admin site', template_mode='bootstrap4')
    admin.add_view(UserModelView())
    admin.add_view(ModelView(Role))
    # admin.add_view(ModelView(User))