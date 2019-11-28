from flask import Blueprint, render_template, redirect, url_for

from app.models import Log
from app.forms import WinnerForm
from app.formatters import format_winners
from app.formatters import format_winner

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
