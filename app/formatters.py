lw_keys = ["name", "nickname", "prize"]


def format_last_winners(last_winners):
    return [dict(zip(lw_keys, lw)) for lw in last_winners]


def format_prizes(prizes):
    return [{"name": p.name} for p in prizes]
