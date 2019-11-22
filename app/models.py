from sqlalchemy.sql.expression import func

from app import db
import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    nickname = db.Column(db.String(255), unique=False, nullable=True)
    maconomy_id = db.Column(db.Integer, unique=True, nullable=False)
    card_id = db.Column(db.Integer, unique=True, nullable=False)
    avatar = db.Column(db.String(255), unique=True, nullable=True)
    chance_modifier = db.Column(db.Float, default=1.0)
    last_spin_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get(cls, card_id):
        return cls.query.filter(cls.card_id == card_id).first()

    def set_chance_modifier(self, config):
        self.chance_modifier = max(
            self.chance_modifier - config.get('USER_CHANCE_MODIFIER'),
            config.get('MIN_USER_CHANCE'))
        db.session.commit()

    def set_last_spin(self):
        self.last_spin_date = datetime.datetime.utcnow()
        db.session.commit()


class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    win = db.Column(db.Boolean())
    prize_id = db.Column(db.Integer, db.ForeignKey("prize.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def add(cls, user_id, win, prize_id=None):
        log = cls(user_id=user_id, win=win, prize_id=prize_id)
        db.session.add(log)
        db.session.commit()

    @classmethod
    def already_played(cls, user_id):
        return cls.query \
            .filter(cls.user_id == user_id) \
            .filter(cls.created_at >= datetime.datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0)) \
            .count() > 0

    @classmethod
    def today_winned_count(cls):
        return cls.today_winned().count()

    @classmethod
    def today_winned(cls):
        return cls.query \
            .filter(cls.win.is_(True)) \
            .filter(cls.created_at >= datetime.datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0))

    @classmethod
    def get_last_winners(cls):
        return cls.query \
            .join(User, cls.user_id == User.id) \
            .join(Prize, cls.prize_id == Prize.id) \
            .with_entities(User.name, User.nickname, Prize.name) \
            .filter(cls.win.is_(True)) \
            .order_by(cls.created_at.desc()) \
            .limit(3) \
            .all()


class Prize(db.Model):
    __tablename__ = "prize"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    picture_url = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get_random(cls):
        today_prizes = [l.prize_id for l in Log.today_winned().all()]
        prize = cls.query \
            .filter(cls.id.notin_(today_prizes)) \
            .order_by(func.random()) \
            .first()
        if not prize:
            return cls.query \
                .order_by(func.random()) \
                .first()
        return prize

    @classmethod
    def get_all(cls):
        return cls.query.all()
