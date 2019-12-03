from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired


class WinnerForm(FlaskForm):
    log_id = HiddenField('id')
    handed_over = SelectField('Megkapta', choices=[('1', 'igen'),
                                                   ('0', 'nem')])
    submit = SubmitField('Küldés')


class PrizeForm(FlaskForm):
    prize_id = HiddenField('prize_id')
    active = SelectField('Aktív', choices=[('1', 'igen'),
                                           ('0', 'nem')])
    submit = SubmitField('Küldés')


class NewPrizeForm(FlaskForm):
    name = StringField('Név', validators=[DataRequired()])
    picture_url = URLField('URL')
    active = SelectField('Aktív', choices=[('1', 'igen'),
                                           ('0', 'nem')])
    submit = SubmitField('Küldés')


class UserForm(FlaskForm):
    card_id = IntegerField('Kártya ID', validators=[DataRequired()])
    maconomy_id = IntegerField('Maconomy ID', validators=[DataRequired()])
    name = StringField('Név', validators=[DataRequired()])
    nickname = StringField('Nicknév')
    avatar = URLField('Avatar')
    active = SelectField('Aktív', choices=[('1', 'igen'),
                                           ('0', 'nem')])
    submit = SubmitField('Küldés')
