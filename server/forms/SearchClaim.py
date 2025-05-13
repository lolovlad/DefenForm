from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import Optional


class SearchClaim(FlaskForm):
    trace_id = StringField('Номер заявки', validators=[Optional()])
    status_id = SelectField('Статус', coerce=int, validators=[Optional()])
    priority_id = SelectField('Приоритет', coerce=int, validators=[Optional()])
    submit = SubmitField('Найти')