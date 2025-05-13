from flask_admin.contrib.sqla import ModelView
from ..database import User
from wtforms import PasswordField
from uuid import uuid4


class UserAdminView(ModelView):
    excluded_list_columns = ("password_hash", )
    form_extra_fields = {
        'password_hash': PasswordField('Пароль')
    }
    form_columns = [
        'name',
        'surname',
        'patronymics',
        'phone',
        'email',
        "password_hash",
        "role",
        "type_service"
    ]
    column_list = [
        'name',
        'surname',
        'patronymics',
        'phone',
        'email',
        "password_hash",
        "role",
        "type_service"]

    column_labels = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'patronymics': 'Отчество',
        'phone': 'Телефон',
        'email': 'Email',
        'password_hash': 'Пароль',
        'role': 'Роль',
        'type_service': 'Тип услуг',
    }

    def on_model_change(self, form, model: User, is_created):
        model.password = form.password_hash.data
        model.trace_id = str(uuid4())