from flask_admin import expose
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, render_template
from wtforms import TextAreaField
from flask_admin.form import rules

from ..database import Contract, Claim, db
from uuid import uuid4

from ..repository import ClaimRepository


class ContractAdminView(ModelView):
    column_labels = {
        'number': "Номер договора",
        'datetime_contract': 'Дата заключения договора',
        'description': 'Описание',
        'terms_and_conditions': 'Условия договора',
        'coast': 'Стоимость (руб.)',
    }
    column_list = [
        'number',
        'datetime_contract',
        'description',
        'terms_and_conditions',
        'coast'
    ]
    form_columns = [
        'number',
        'datetime_contract',
        'description',
        'terms_and_conditions',
        'coast',
    ]
    form_overrides = {
        'description': TextAreaField,
        'terms_and_conditions': TextAreaField
    }

    @expose('/create_from_claim/<int:claim_id>/', methods=['GET', 'POST'])
    def create_from_claim(self, claim_id):
        repo = ClaimRepository(db.session)
        claim = repo.get(claim_id)

        contract = self.model(id_claim=claim.id, trace_id=str(uuid4()))
        status = repo.get_state_claim_bu_name("В работе")
        form = self.create_form(obj=contract)

        if self.validate_form(form):
            self._on_model_change(form, contract, True)
            form.populate_obj(contract)
            claim.id_status = status.id
            repo.edit(claim)
            self.session.add(contract)
            self._on_model_change(form, contract, True)
            self.session.commit()
            return redirect(self.get_url('.index_view'))

        return self.render('admin/model/create.html', form=form, form_args=self.form_args,
                           return_url=request.referrer)

    def on_model_change(self, form, model: Claim, is_created):
        model.trace_id = str(uuid4())