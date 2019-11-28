from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, SubmitField


class WinnerForm(FlaskForm):
    log_id = HiddenField('id')
    handed_over = SelectField('Megkapta', choices=[('1', 'igen'),
                                                   ('0', 'nem')])
    submit = SubmitField('Küldés')
