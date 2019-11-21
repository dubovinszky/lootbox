from flask import Blueprint, jsonify

from app import app
from app import db
from app.models import User
from app.models import Log
from app.models import Prize
from app.utils import win
from app.utils import get_daily_modifier

api = Blueprint('api', __name__)


def _make_response(json):
    resp = jsonify(json)
    resp.headers.add_header('Access-Control-Allow-Origin', '*')
    return resp


def _msg(success, msg, **kwargs):
    return {"success": success, "msg": msg, **kwargs}


@api.route('/get_user/<card_id>', methods=['GET'])
def get_user(card_id):
    user = User.get(card_id)
    if not user:
        return _msg(False, "user does not exist")
    return _msg(True, "", name=user.name, nickname=user.nickname,
                maconomy_id=user.maconomy_id, avatar=user.avatar,
                already_played=Log.already_played(user.id))


@api.route('/spin/<card_id>', methods=['GET'])
def spin(card_id):
    user = User.get(card_id)
    if not user:
        return _msg(False, "user does not exist")

    already_played = Log.already_played(user.id)
    if already_played:
        return _msg(False, "already played",
                    already_played=already_played)

    today_winned = Log.today_winned_count()
    if today_winned >= app.config.get('PRIZES_PER_DAY'):
        return _msg(False, "no more prizes")

    winner = win(app.config, user.chance_modifier,
                 get_daily_modifier(app.config, today_winned))
    if winner:
        prize = Prize.get_random()

        user.chance_modifier = max(
            user.chance_modifier - app.config.get('USER_CHANCE_MODIFIER'),
            app.config.get('MIN_USER_CHANCE'))
        log = Log(user_id=user.id, win=True, prize_id=prize.id)
        db.session.add(log)
        db.session.commit()

        return _msg(True, "win", prize=prize.name)

    log = Log(user_id=user.id, win=False)
    db.session.add(log)
    db.session.commit()

    return _msg(False, "no win")
