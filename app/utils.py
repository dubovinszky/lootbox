import secrets

from flask import jsonify


def get_random():
    return secrets.SystemRandom().random()


def win(config, chance_modifier, today_winned):
    chance = get_random() \
        * chance_modifier \
        * _get_daily_modifier(config, today_winned)
    return chance >= config.get('WIN_LIMIT')


def _get_daily_modifier(config, today_winned):
    return max(1 - today_winned * config.get('DAILY_MODIFIER'),
               config.get('MIN_DAILY_MODIFIER'))


def _make_response(json):
    resp = jsonify(json)
    resp.headers.add_header('Access-Control-Allow-Origin', '*')
    return resp


def msg(success, **kwargs):
    return _make_response({"success": success, **kwargs})
