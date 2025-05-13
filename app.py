from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_uuid import FlaskUUID
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel

from server.database import *
from server.models import UserSession

from server.repository import UserRepository
from server.models import GetUser
from server.service import LoginService, UserService, ClaimService

from server.admin_view import *

from server.forms import LoginForm, RegistrationForm

from server.blueprints.user.user import user_router
from server.blueprints.worker.worker import worker_router

app = Flask(__name__)
babel = Babel(app)
app.config['SECRET_KEY'] = '2wae3tgv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

app.config['UPLOAD_FOLDER'] = '/Files'


app.register_blueprint(user_router, name="user_blueprint", url_prefix="/user")
app.register_blueprint(worker_router, name="worker_blueprint", url_prefix="/worker")

flask_uuid = FlaskUUID()

db.init_app(app)
flask_uuid.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

migrate = Migrate(app, db, render_as_batch=True)


def get_locale():
    return 'ru'


babel.init_app(app, locale_selector=get_locale)

route = {
    "worker": "worker_blueprint.index",
    "admin": "/admin",
    "user": "/"
}

menu = [
    {"url": "index", "title": "главная"},
]


@login_manager.user_loader
def load_user(id_user) -> UserSession:
    repo = UserRepository(db.session)
    try:
        return UserSession(GetUser.model_validate(repo.get_user(int(id_user)), from_attributes=True))
    except:
        return UserSession(None)


@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        user_roles = current_user.user.role.name
        if "worker" in user_roles:
            return redirect(url_for(route["worker"]))
        elif "admin" in user_roles:
            return redirect(route["admin"])
        else:
            return render_template("index.html", exception="", menu=menu, user=current_user)

    else:
        return render_template("index.html", exception="", menu=menu, user=current_user)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            login_service = LoginService()
            user = login_service.login_user(form.email.data, form.password.data)
            if user is None:
                return redirect("login")
            login_user(UserSession(user))
            session["car"] = {}
            return redirect("/")
        return redirect("login")


@app.route("/claim_detail/<uuid>", methods=["GET"])
def claim_detail(uuid: str):
    service = ClaimService()
    claim = service.get_claim_by_uuid(uuid)
    contract = service.get_contract_by_id_claim(claim.id)
    return render_template("info_claim.html",
                           menu=menu,
                           user=current_user,
                           claim=claim,
                           contract=contract)


@app.route("/registration", methods=["POST", "GET"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    user_service = UserService()
    form.type_service.choices = [(stype.id, stype.name) for stype in user_service.get_list_type_service()]
    if request.method == "GET":
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)
    if request.method == "POST":
        if form.validate_on_submit():
            user = user_service.registration(
                form.name.data,
                form.surname.data,
                form.patronymics.data,
                form.phone.data,
                form.email.data,
                form.password.data,
                form.type_service.data
            )
            login_user(UserSession(user))
            session["car"] = {}
            return redirect(url_for('index'))
        return render_template("registration.html", title="Авторизация", form=form, menu=menu, user=current_user)


@app.route("/init_app/<password>", methods=["GET"])
def create_user_admin(password):
    if request.method == "GET":
        if password == "AdminCreate":
            roles = [
                Role(
                    name="worker",
                    description="worker"
                ),
                Role(
                    name="admin",
                    description="admin"
                ),
                Role(
                    name="user",
                    description="user"
                ),
            ]
            type_service = [
                TypeService(
                    name="Патрулирование"
                ),
                TypeService(
                    name="Охрана объектов"
                ),
                TypeService(
                    name="Cопровождение грузов"
                )
            ]
            service_selection = [
                ServiceSelection(
                    name="Охрана объектов",
                ),
                ServiceSelection(
                    name="Личная охрана",
                ),
                ServiceSelection(
                    name="Видеонаблюдение",
                ),
                ServiceSelection(
                    name="Охрана мероприятий",
                )
            ]
            priority = [
                Priority(
                    name="Низший",
                    coast=1
                ),
                Priority(
                    name="Обычный",
                    coast=2
                ),
                Priority(
                    name="Высший",
                    coast=3
                )
            ]
            status = [
                Status(
                    name="В обработке"
                ),
                Status(
                    name="В работе"
                ),
                Status(
                    name="Закрыта"
                )
            ]

            db.session.add_all(roles)
            db.session.add_all(type_service)
            db.session.add_all(service_selection)
            db.session.add_all(priority)
            db.session.add_all(status)
            db.session.commit()

            admin_user = User(
                name="Иван",
                surname="Иван",
                patronymics="Иван",
                phone="9033499161",
                email="admin@admin.ru",
                role=roles[1]
            )
            admin_user.password = "admin"

            db.session.add(admin_user)
            db.session.commit()

            return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


admin = Admin(app, name="Панель Админ", index_view=MyAdminIndexView())

admin.add_view(UserAdminView(User, db.session, name="Пользователь"))
admin.add_view(ClaimAdminView(Claim, db.session, name="Заявки"))
admin.add_view(ContractAdminView(Contract, db.session, name="Договора", endpoint='contractadminview'))
admin.add_view(ModelView(TypeService, db.session, name="Тип сервиса"))
admin.add_view(ModelView(ServiceSelection, db.session, name="Предоставляемые услуги"))


admin.add_link(LogoutMenuLink(name="Выход", category="", url="/logout"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
