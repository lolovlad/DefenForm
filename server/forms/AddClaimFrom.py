from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class AddClaimForm(FlaskForm):
    datetime_claim = DateTimeField("Дата и время заявки", format="%Y-%m-%dT%H:%M")
    address = StringField("Адрес", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    id_service_selection = SelectField("Тип сервиса", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Оставить заявку")
