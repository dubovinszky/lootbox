lw_keys = ["name", "nickname", "prize"]
w_keys = ["id", "card_id", "name", "prize", "handed_over", "date"]


def format_last_winners(last_winners):
    return [dict(zip(lw_keys, lw)) for lw in last_winners]


def format_prizes(prizes):
    return [{"id": p.id, "name": p.name, "active": p.active} for p in prizes]


def format_winners(winners):
    return [format_winner(w) for w in winners]


def format_winner(winner):
    return dict(zip(w_keys, winner))
