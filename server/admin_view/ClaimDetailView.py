from flask_admin import BaseView, expose
from flask import render_template, redirect, url_for
from ..database import Claim, Contract
from flask_login import login_required
from flask_admin import AdminIndexView
from app import db


class ClaimDetailView(BaseView):
    @expose('/<int:claim_id>')
    def index(self, claim_id):
        claim = db.session.get(Claim, claim_id)
        contract = db.session.query(Contract).filter_by(id_claim=claim_id).first()
        return render_template("admin/claim_detail.html", claim=claim, contract=contract)