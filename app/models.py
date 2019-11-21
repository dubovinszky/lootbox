from sqlalchemy.sql.expression import func

from app import db
import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    nickname = db.Column(db.String(255), unique=True, nullable=True)
    maconomy_id = db.Column(db.Integer, unique=True, nullable=False)
    card_id = db.Column(db.Integer, unique=True, nullable=False)
    avatar = db.Column(db.String(255), unique=True, nullable=True)
    chance_modifier = db.Column(db.Float, default=1.0)
    last_spin_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get(cls, card_id):
        return cls.query.filter(cls.card_id == card_id).first()


class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    win = db.Column(db.Boolean())
    prize_id = db.Column(db.Integer, db.ForeignKey("prize.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def already_played(cls, user_id):
        return cls.query \
            .filter(cls.user_id == user_id) \
            .filter(cls.created_at >= datetime.datetime.now().replace(
                hour=0, minute=0,
                second=0, microsecond=0)) \
            .count() > 0

    @classmethod
    def today_winned_count(cls):
        return cls.query \
            .filter(cls.win.is_(True)) \
            .filter(cls.created_at >= datetime.datetime.now().replace(
                hour=0, minute=0,
                second=0, microsecond=0)) \
            .count()


class Prize(db.Model):
    __tablename__ = "prize"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    picture_url = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get_random(cls):
        return cls.query \
            .order_by(func.random()) \
            .first()
