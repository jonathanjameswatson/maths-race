from flask import Blueprint

from mathsrace.db import get_db

main = Blueprint('main', __name__, url_prefix='/', template_folder='templates')


def get_leaderboard(number):
    database = get_db()

    return database.execute('''
        SELECT user.username, score.score
        FROM score
        INNER JOIN user ON score.user_id=user.id
        ORDER BY score.score DESC
        LIMIT ?
    ''', (number,)).fetchall()


from . import views
