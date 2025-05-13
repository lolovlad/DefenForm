from uuid import uuid4
from flask_admin.contrib.sqla import ModelView



#class WorkshopAdminView(ModelView):
#
#    form_columns = [
#        'name',
#        'address',
#        'description'
#    ]
#
#    def on_model_change(self, form, model: Workshop, is_created):
#        model.trace_id = str(uuid4())