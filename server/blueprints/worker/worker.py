from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required


from server.forms import SearchClaim
from server.service import ClaimService


worker_router = Blueprint("worker", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "worker_blueprint.list_claim", "title": "Заявки"},
]


@worker_router.before_request
def is_worker():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "worker" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@worker_router.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html", menu=menu, user=current_user)


@worker_router.route("/list_claim", methods=['GET', 'POST'])
@login_required
def list_claim():
    service = ClaimService()
    form = SearchClaim(request.args)

    form.status_id.choices = [(-1, 'Все')] + [(s.id, s.name) for s in service.get_status_all()]
    form.priority_id.choices = [(-1, 'Все')] + [(p.id, p.name) for p in service.get_priority_all()]

    if form.trace_id.data:
        trace_id = form.trace_id.data.strip()
    else:
        trace_id = None

    status_id = form.status_id.data if form.status_id.data else -1
    priority_id = form.priority_id.data if form.priority_id.data else -1
    list_claim = service.get_claim_work_search(current_user.user.id, trace_id, status_id, priority_id)
    return render_template("list_claim_worker.html", form=form, menu=menu, user=current_user, claims=list_claim)


@worker_router.route('/change_status')
@login_required
def change_status():
    trace_id = request.args.get('trace_id')
    service = ClaimService()
    is_edit = service.change_status(trace_id)
    if not is_edit:
        flash("Заявка не найдена", "error")
        return redirect(url_for('.list_claim'))

    flash("Статус заявки обновлён", "success")
    return redirect(url_for('.list_claim'))



