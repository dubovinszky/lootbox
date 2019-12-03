from sqlalchemy.sql.expression import func

from app import db
import datetime


class Base():
    @classmethod
    def get(cls, _id):
        return cls.query.filter(cls.id == _id).first()


class User(Base, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    nickname = db.Column(db.String(255), unique=False, nullable=True)
    maconomy_id = db.Column(db.Integer, unique=True, nullable=False)
    card_id = db.Column(db.Integer, unique=True, nullable=False)
    avatar = db.Column(db.String(255), unique=True, nullable=True)
    chance_modifier = db.Column(db.Float, default=1.0)
    last_spin_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, server_default='t', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get_by_card_id(cls, card_id):
        return cls.query.filter(cls.card_id == card_id) \
            .filter(cls.active.is_(True)) \
            .first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.card_id).all()

    def set_chance_modifier(self, config):
        self.chance_modifier = max(
            self.chance_modifier - config.get('USER_CHANCE_MODIFIER'),
            config.get('MIN_USER_CHANCE'))
        db.session.commit()

    def get_chance_modifier(self, config):
        def _reset():
            return ((datetime.datetime.utcnow() - last_win.created_at).days >
                    config.get('USER_CHANCE_RESET_DAYS'))

        last_win = Log.query \
            .filter(Log.user_id == self.id) \
            .filter(Log.win.is_(True)) \
            .order_by(Log.created_at.desc()) \
            .first()

        if last_win and _reset():
            self.chance_modifier = 1.0
            db.session.commit()
        return self.chance_modifier

    def set_last_spin(self):
        self.last_spin_date = datetime.datetime.utcnow()
        db.session.commit()

    @classmethod
    def new(cls, card_id, maconomy_id, name, nickname, avatar, active):
        user = cls(card_id=card_id, maconomy_id=maconomy_id, name=name,
                   nickname=nickname, avatar=avatar, active=active)
        db.session.add(user)
        db.session.commit()

    def update(self, card_id, maconomy_id, name, nickname, avatar, active):
        self.card_id = card_id
        self.maconomy_id = maconomy_id
        self.name = name
        self.nickname = nickname
        self.avatar = avatar
        self.active = active
        db.session.commit()


class Log(Base, db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    win = db.Column(db.Boolean())
    prize_id = db.Column(db.Integer, db.ForeignKey("prize.id"), nullable=True)
    handed_over = db.Column(db.Boolean(), server_default='f', nullable=False)
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
    def winners(cls):
        return cls.query \
            .join(User, cls.user_id == User.id) \
            .join(Prize, cls.prize_id == Prize.id) \
            .with_entities(Log.id, User.card_id, User.name, Prize.name,
                           Log.handed_over, Log.created_at) \
            .filter(cls.win.is_(True)) \
            .order_by(cls.handed_over, cls.created_at.desc()) \
            .all()

    @classmethod
    def winner(cls, log_id):
        return cls.query \
            .join(User, cls.user_id == User.id) \
            .join(Prize, cls.prize_id == Prize.id) \
            .with_entities(Log.id, User.card_id, User.name, Prize.name,
                           Log.handed_over, Log.created_at) \
            .filter(cls.id == log_id) \
            .first()

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

    def hand_over(self, handed_over):
        self.handed_over = handed_over
        db.session.commit()


class Prize(Base, db.Model):
    __tablename__ = "prize"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    picture_url = db.Column(db.String(255), unique=True, nullable=True)
    active = db.Column(db.Boolean, server_default='t', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def add(cls, name, picture_url, active):
        prize = Prize(name=name, picture_url=picture_url, active=active)
        db.session.add(prize)
        db.session.commit()

    @classmethod
    def get_random(cls):
        today_prizes = [l.prize_id for l in Log.today_winned().all()]
        prize = cls.query \
            .filter(cls.id.notin_(today_prizes)) \
            .filter(cls.active.is_(True)) \
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

    def set_status(self, active):
        self.active = active
        db.session.commit()
