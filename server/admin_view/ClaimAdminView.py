from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import LinkRowAction
from flask_admin.form import ImageUploadField, FileUploadField
from random import getrandbits

from markupsafe import Markup
from ..database import Claim, User, Role, Priority, Status

from uuid import uuid4
import os
import os.path as op
from flask import url_for

from werkzeug.utils import secure_filename


file_path = os.path.abspath(os.path.dirname(__name__))


def contract_button(view, context, model, name):
    if model.contract is None:
        return Markup(
            f'<a class="btn btn-sm btn-primary" href="{url_for("contractadminview.create_from_claim", claim_id=model.id)}">'
            f'Заключить договор</a>'
        )
    return ''


def list_description(view, content, model: Claim, name):
    text = model.description
    if len(model.description) > 40:
        text = model.description[:41] + "..."
    return Markup(f"<p>{text}</p>")


class ClaimAdminView(ModelView):
    edit_modal = True
    can_view_details = True
    details_template = 'admin/claim_detail.html'
    form_columns = [
        'datetime_claim',
        'address',
        'user',
        'worker',
        'service_selection',
        'status',
    ]
    form_args = {
        'worker': {
            'query_factory': lambda: User.query.join(Role).filter(Role.name == 'worker').all(),
            'allow_blank': True,
            'get_label': lambda user: f"{user.surname} {user.name}"
        }
    }
    column_sortable_list = [
        ('datetime_claim', 'datetime_claim'),
        ('status', 'status.name'),
        ('priority', 'priority.coast'),
    ]
    column_formatters = {
        "description": list_description,
        'contract_action': contract_button
    }
    column_list = ['trace_id',
                   'datetime_claim',
                   'service_selection',
                   'description',
                   'status',
                   'priority',
                   'contract_action']

    column_labels = {
        'trace_id': 'Номер заявки',
        'datetime_claim': 'Дата и время',
        'service_selection': 'Услуга',
        'description': 'Описание',
        'status': 'Статус',
        'priority': 'Приоритет',
        'contract_action': 'Договор',
        'address': 'Адрес',
        'user': 'Клиент',
        'worker': 'Сотрудник',
    }

    column_searchable_list = [
        'trace_id',
        'address',
        'description',
    ]

    def create_form(self, obj=None):
        return super(ClaimAdminView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(ClaimAdminView, self).edit_form(obj)

    def on_model_change(self, form, model: Claim, is_created):
        model.trace_id = str(uuid4())
