from flask import render_template, g

from ..main import main
from . import get_leaderboard


@main.route('/')
def index():
    if g.user:
        return render_template('main/main.html.j2', lb=get_leaderboard(5))
    return render_template('main/intro.html.j2', lb=get_leaderboard(5))
