# Create customized model view class
from flask_admin.contrib.mongoengine import ModelView as MV
from flask_admin import AdminIndexView as AIV

from flask_security import current_user
from flask import abort, redirect, url_for, request, current_app
from ..user.models import Role

class SecurityMixin(object):
    def is_accessible(self):
        return (
            current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role(Role.admin_name)
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                sbpn = current_app.config['SECURITY_BLUEPRINT_NAME']
                return redirect(url_for(f'{sbpn}.login', next=request.url))


class ModelView(SecurityMixin, MV):
    def __init__(self, *a, **kw):
        '''一个小技巧，实现可以使用 class attribute `model_class` 指定模型。
        '''
        try:
            model = self.model_class
        except AttributeError:
            # 兼容原来在构建实例时指定模型的写法。
            model = kw.pop('model', None)
            if model is None:
                model, *a = a
        super().__init__(model, *a, **kw)


class AdminIndexView(SecurityMixin, AIV):
    pass
