from ...admin import admin, ModelView
from .models import EventLog


class EventLogModelView(ModelView):
    model_class = EventLog

    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_filters = ['predicate', 'subject', 'occurred_at']


admin.add_view(EventLogModelView())
