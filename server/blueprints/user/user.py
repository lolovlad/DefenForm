from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import current_user, login_required

from server.forms import AddClaimForm
from server.service import ClaimService


user_router = Blueprint("user", __name__, template_folder="templates", static_folder="static")


menu = [
    {"url": "index", "title": "главная"},
]


@user_router.before_request
def is_user():
    if current_user.is_authenticated:
        user_role = current_user.user.role.name
        if "user" != user_role:
            return redirect("/")
    else:
        return redirect("/")


@user_router.route("/list_claim", methods=["GET"])
@login_required
def list_claim():
    service = ClaimService()
    list_claim = service.get_claim_by_user(current_user.user.id)
    return render_template("list_claim.html", menu=menu, user=current_user, claims=list_claim)


@user_router.route("/add_claim", methods=["GET", "POST"])
@login_required
def add_claim():
    service = ClaimService()
    form = AddClaimForm()
    form.id_service_selection.choices = [(s.id, s.name) for s in service.get_all_service_selection()]
    if request.method == "GET":
        return render_template("add_claim.html", menu=menu, user=current_user, form=form)
    else:
        if form.validate_on_submit():
            print(form)
            entity = service.add_claim(form, current_user.user.id)
            print(entity)
            return redirect(url_for("user_blueprint.list_claim"))
        return render_template("add_claim.html", menu=menu, user=current_user, form=form)


#@user_router.route("/info_order/<uuid>", methods=["GET"])
#@login_required
#def info_order(uuid: str):
#    service = ShopService()
#    order = service.get_order_by_uuid(uuid)
#    return render_template("info_order.html", menu=menu, user=current_user, order=order, type_order=type_order, state_order=state_order)
#
#
#@user_router.route("/create_order", methods=["GET", "POST"])
#@login_required
#def create_order():
#    form = CreateOrderForm()
#    service = ShopService()
#    workshop = service.get_list_workshop()
#    form.workshops.choices = [(g.trace_id, g.name) for g in workshop]
#    if request.method == "GET":
#        cart = session.get("car")
#        form.type_order.data = 1
#        order_sweet_product = service.get_list_product_by_uuid(list(cart.keys()), cart)
#        sum_cart = 0
#        for prod in order_sweet_product:
#            sum_cart += prod.count * prod.price
#
#        return render_template("create_order.html",
#                               menu=menu,
#                               user=current_user,
#                               form=form,
#                               sum_cart=sum_cart,
#                               products=order_sweet_product)
#    elif request.method == "POST":
#            address = ""
#            type_order = TypeOrder.in_hall
#            if int(form.type_order.data) == TypeOrder.in_hall.value:
#                address = service.get_address_by_workshop_uuid(form.workshops.data)
#                print("Тип заказа: в зале")
#            else:
#                type_order = TypeOrder.with_myself
#                address = f"{form.city.data} {form.street.data} {form.home.data} {form.apartment.data} {form.floor.data}"
#                print("Тип заказа: Доставка")
#            cart = session.get("car")
#            order = service.create_order(type_order, address, form.description.data, cart, current_user.user.id)
#            if order is not None:
#                session["car"] = {}
#                return redirect(url_for('user_blueprint.info_order',  uuid=order.trace_id))
#            else:
#                return redirect(url_for("user_blueprint.create_order"))