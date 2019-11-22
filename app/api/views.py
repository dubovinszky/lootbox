from flask import Blueprint, jsonify

from app import app
from app.models import User
from app.models import Log
from app.models import Prize
from app.utils import win
from app.utils import get_daily_modifier
from app.formatters import format_last_winners
from app.formatters import format_prizes

api = Blueprint('api', __name__)


def _make_response(json):
    resp = jsonify(json)
    resp.headers.add_header('Access-Control-Allow-Origin', '*')
    return resp


def _msg(success, **kwargs):
    return _make_response({"success": success, **kwargs})


@api.route('/get_user/<card_id>', methods=['GET'])
def get_user(card_id):
    user = User.get(card_id)
    if not user:
        return _msg(False, msg="user does not exist")
    return _msg(True, name=user.name, nickname=user.nickname,
                maconomy_id=user.maconomy_id, avatar=user.avatar,
                already_played=Log.already_played(user.id))


@api.route('/spin/<card_id>', methods=['GET'])
def spin(card_id):
    user = User.get(card_id)
    if not user:
        return _msg(False, msg="user does not exist")

    # PRESENTATION_MODE
    if app.config.get('PRESENTATION_MODE') and \
            user.card_id == app.config.get('PRESENTATION_ID'):
        prize = Prize.get_random()
        Log.add(user_id=user.id, win=True, prize_id=prize.id)
        return _msg(True, prize=prize.name)

    already_played = Log.already_played(user.id)
    if already_played:
        return _msg(False, msg="already played",
                    already_played=already_played)

    today_winned = Log.today_winned_count()
    if today_winned >= app.config.get('PRIZES_PER_DAY'):
        return _msg(False, msg="no more prizes")

    winner = win(app.config, user.chance_modifier,
                 get_daily_modifier(app.config, today_winned))
    if winner:
        prize = Prize.get_random()

        user.set_chance_modifier(app.config)
        Log.add(user_id=user.id, win=True, prize_id=prize.id)

        return _msg(True, prize=prize.name)

    Log.add(user_id=user.id, win=False)

    return _msg(False, msg="no win")


@api.route('/last_winners', methods=['GET'])
def get_last_winners():
    return _msg(True, last_winners=format_last_winners(Log.get_last_winners()))


@api.route('/prizes', methods=['GET'])
def get_prizes():
    return _msg(True, prizes=format_prizes(Prize.get_all()))
