from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchOrderWorkerForm(FlaskForm):
    state_order = SelectField("Статус заказа", choices=[
        ("confirmed", "Подтверждено"),
        ("prepared", "Сборка"),
        ("ready", "Готово"),
        ("waiting_for_the_courier", "Ждет отгрузки")
    ])
    type_order = SelectField("Тип заказа", choices=[
        ("in_hall", "Со склада"),
        ("with_myself", "Доставка")
    ])
    submit = SubmitField("Найти")