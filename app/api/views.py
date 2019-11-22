from flask import Blueprint

from app import app
from app.models import Log
from app.models import Prize
from app.utils import win
from app.utils import get_daily_modifier
from app.utils import msg
from app.formatters import format_last_winners
from app.formatters import format_prizes
from app.decorators import user_check
from app.decorators import presentation_mode_spin
from app.decorators import presentation_mode_get_user

api = Blueprint('api', __name__)


@api.route('/get_user/<card_id>', methods=['GET'])
@user_check()
@presentation_mode_get_user()
def get_user(user, card_id):
    return msg(True, name=user.name, nickname=user.nickname,
               maconomy_id=user.maconomy_id, avatar=user.avatar,
               already_played=Log.already_played(user.id),
               last_spin=user.last_spin_date)


@api.route('/spin/<card_id>', methods=['GET'])
@user_check()
@presentation_mode_spin()
def spin(user, card_id):
    already_played = Log.already_played(user.id)
    if already_played:
        return msg(False, msg="already played",
                   already_played=already_played)

    user.set_last_spin()
    today_winned = Log.today_winned_count()
    if today_winned >= app.config.get('PRIZES_PER_DAY'):
        return msg(False, msg="no more prizes")

    winner = win(app.config, user.chance_modifier,
                 get_daily_modifier(app.config, today_winned))
    if winner:
        prize = Prize.get_random()

        user.set_chance_modifier(app.config)
        Log.add(user_id=user.id, win=True, prize_id=prize.id)

        return msg(True, prize=prize.name, prize_id=prize.id)

    Log.add(user_id=user.id, win=False)

    return msg(False, msg="no win")


@api.route('/last_winners', methods=['GET'])
def get_last_winners():
    return msg(True, last_winners=format_last_winners(Log.get_last_winners()))


@api.route('/prizes', methods=['GET'])
def get_prizes():
    return msg(True, prizes=format_prizes(Prize.get_all()))
