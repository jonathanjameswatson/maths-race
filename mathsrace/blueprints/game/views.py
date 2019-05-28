from flask import render_template

from ..game import game
from mathsrace.blueprints.auth import login_required


@game.route('/')
@login_required
def index():
    return render_template('game/game.html.j2')
