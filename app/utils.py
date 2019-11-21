import secrets


def get_random():
    return secrets.SystemRandom().random()


def win(config, chance_modifier, daily_modifier):
    chance = get_random() * chance_modifier * daily_modifier
    return chance >= config.get('WIN_LIMIT')


def get_daily_modifier(config, today_winned):
    return 1 - today_winned * config.get('DAILY_MODIFIER')
