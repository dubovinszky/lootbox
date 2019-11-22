from functools import wraps

from flask import abort

from app import app
from app.models import User
from app.models import Prize
from app.models import Log
from app.utils import msg


def user_check():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            card_id = kwargs.get('card_id')
            user = User.get(card_id)
            if not user:
                abort(msg(False, msg="user does not exist"))
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator


def presentation_mode_get_user():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = args[0]
            if app.config.get('PRESENTATION_MODE') and \
                    user.card_id == app.config.get('PRESENTATION_ID'):
                abort(msg(True, name=user.name, nickname=user.nickname,
                          maconomy_id=user.maconomy_id, avatar=user.avatar,
                          already_played=False,
                          last_spin=user.last_spin_date))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def presentation_mode_spin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = args[0]
            if app.config.get('PRESENTATION_MODE') and \
                    user.card_id == app.config.get('PRESENTATION_ID'):
                prize = Prize.get_random()
                Log.add(user_id=user.id, win=True, prize_id=prize.id)
                user.set_last_spin()
                abort(msg(True, prize=prize.name, prize_id=prize.id))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
