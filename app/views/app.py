from flask import Blueprint, render_template, redirect, url_for

from app.models import Log
from app.models import Prize
from app.models import User
from app.forms import WinnerForm
from app.forms import PrizeForm
from app.forms import NewPrizeForm
from app.forms import UserForm
from app.formatters import format_winners
from app.formatters import format_winner
from app.formatters import format_prizes

app_bp = Blueprint('app', __name__)


@app_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', winners=format_winners(Log.winners()))


@app_bp.route('/winner/<log_id>', methods=['GET'])
def winner(log_id):
    winner = format_winner(Log.winner(log_id))
    form = WinnerForm(log_id=winner['id'],
                      handed_over=1 if winner['handed_over'] else 0)
    return render_template('winner.html', winner=winner, form=form)


@app_bp.route('/winner/<log_id>', methods=['POST'])
def winner_update(log_id):
    form = WinnerForm()
    if form.validate_on_submit():
        winner = Log.get(log_id)
        winner.hand_over(True if form.handed_over.data == "1" else False)

    return redirect(url_for('app.index'))


@app_bp.route('/prizes', methods=['GET'])
def prizes():
    return render_template('prizes.html',
                           prizes=format_prizes(Prize.get_all()))


@app_bp.route('/prizes/new', methods=['GET', 'POST'])
def prizes_new():
    form = NewPrizeForm()
    if form.validate_on_submit():
        Prize.add(name=form.name.data, picture_url=form.picture_url.data,
                  active=True if form.active.data == "1" else False)
        return redirect(url_for('app.prizes'))
    return render_template('prizes_new.html', form=form)


@app_bp.route('/prize/<prize_id>', methods=['GET'])
def prize(prize_id):
    prize = Prize.get(prize_id)
    form = PrizeForm(prize_id=prize.id, active=1 if prize.active else 0)
    return render_template('prize.html', prize=prize, form=form)


@app_bp.route('/prize/<prize_id>', methods=['POST'])
def prize_update(prize_id):
    form = PrizeForm()
    if form.validate_on_submit():
        prize = Prize.get(prize_id)
        prize.set_status(True if form.active.data == "1" else False)

    return redirect(url_for('app.prizes'))


@app_bp.route('/users', methods=['GET'])
def users():
    return render_template('users.html', users=User.get_all())


@app_bp.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    user = User.get(user_id)
    form = UserForm(card_id=user.card_id, maconomy_id=user.maconomy_id,
                    name=user.name, nickname=user.nickname, avatar=user.avatar,
                    active=1 if user.active else 0)
    return render_template('user.html', form=form)


@app_bp.route('/user/<user_id>', methods=['POST'])
def user_update(user_id):
    form = UserForm()
    if form.validate_on_submit():
        user = User.get(user_id)
        user.update(
            card_id=form.card_id.data, maconomy_id=form.maconomy_id.data,
            name=form.name.data, nickname=form.nickname.data,
            avatar=form.avatar.data,
            active=True if form.active.data == '1' else False)
        return redirect(url_for('app.users'))
    return render_template('user.html', form=form)


@app_bp.route('/users/new', methods=['GET', 'POST'])
def user_new():
    form = UserForm()
    if form.validate_on_submit():
        User.new(
            card_id=form.card_id.data, maconomy_id=form.maconomy_id.data,
            name=form.name.data, nickname=form.nickname.data,
            avatar=form.avatar.data,
            active=True if form.active.data == '1' else False)
        return redirect(url_for('app.users'))
    return render_template('user.html', form=form)
