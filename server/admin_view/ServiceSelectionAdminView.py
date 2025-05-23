from flask_admin.contrib.sqla import ModelView


class ServiceSelectionAdminView(ModelView):
    form_columns = [
        'name',
        'description'
    ]
    column_list = [
        'name',
        'description'
    ]

    column_labels = {
        'name': 'Название',
        'description': 'Описание',
    }