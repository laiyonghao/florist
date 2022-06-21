# Create customized model view class
from flask_admin.contrib.mongoengine import ModelView as MV
from flask_admin import AdminIndexView as AIV

from flask_security import current_user
from flask import abort, redirect, url_for, request

class SecurityMixin(object):
    def is_accessible(self):
        return (
            current_user.is_active and
            current_user.is_authenticated and
            current_user.has_role('admin')
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
                return redirect(url_for('security.login', next=request.url))


class ModelView(SecurityMixin, MV):
    pass


class AdminIndexView(SecurityMixin, AIV):
    pass
