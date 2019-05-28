from flask import Blueprint
from flask_socketio import close_room, emit
from random import randint

from mathsrace.db import get_db

game = Blueprint('game', __name__, url_prefix='/game',
                 template_folder='templates', static_folder='static')


def create_question():
    a = randint(1, 50)
    b = randint(1, 50)
    return [a, b, a + b]


def init_game(number, host_id):
    db = get_db()

    game_id = db.execute('''
        INSERT INTO game (num_of_questions, host_id) VALUES (?, ?)
    ''', (number, host_id)).lastrowid

    for i in range(number):
        q = create_question()

        db.execute('''
            INSERT INTO question (game_id, num, a, b, answer)
            VALUES (?, ?, ?, ?, ?)
        ''', (game_id, i, q[0], q[1], q[2]))

    db.commit()

    return game_id


def add_to_user_game(user_id, game_id):
    db = get_db()

    db.execute('''
        INSERT OR IGNORE INTO user_game (user_id, game_id)
        VALUES (?, ?)
    ''', (user_id, game_id,))

    db.commit()

    host = db.execute('''
        SELECT user.username FROM user, game
        WHERE game.id = ? AND user.id = game.host_id
    ''', (game_id,)).fetchall()

    player_list = db.execute('''
        SELECT user.username FROM user, user_game
        WHERE user_game.game_id = ? AND user.id = user_game.user_id
    ''', (game_id,)).fetchall()

    return ([row[0] for row in host], [row[0] for row in player_list])


def close_game(game_id):
    db = get_db()

    db.execute('DELETE FROM game WHERE id = ?', (game_id,))
    db.execute('DELETE FROM question WHERE game_id = ?', (game_id,))
    emit('room_closed', room=game_id)
    close_room(game_id)

    db.commit()


def remove_user(user_id):
    db = get_db()

    db.execute('DELETE FROM user_game WHERE user_id = ?', (user_id,))

    db.commit()


def leave_game(user_id):
    db = get_db()

    username = db.execute('''SELECT username FROM user WHERE id = ?''',
                          (user_id,)).fetchone()[0]

    game_id = db.execute('''SELECT game_id FROM user_game WHERE user_id = ?''',
                         (user_id,)).fetchone()

    if game_id is None:
        console.log("NADA")
        return None

    game_id = game_id['game_id']

    remove_user(user_id)
    emit('user_left', username, room=game_id, include_self=False)

    host_id = db.execute('''
        SELECT host_id FROM game WHERE host_id = ?
    ''', (user_id,)).fetchone()

    if host_id is not None:
        all_user_ids = db.execute('''
            SELECT user_id FROM user_game WHERE game_id = ?
        ''', (game_id,)).fetchall()

        for all_user_id in all_user_ids:
            remove_user(all_user_id['user_id'])

    game_id_check = db.execute('''
        SELECT game_id FROM user_game WHERE game_id = ?
    ''', (game_id,)).fetchone()

    if game_id_check is None:
        emit('room_closed', room=game_id)
        close_game(game_id)

    db.commit()


def find_game(host_name):
    db = get_db()

    game_id = db.execute('''
        SELECT game.id FROM game, user
        WHERE user.username = ? AND game.host_id = user.id
        ''', (host_name,)).fetchone()

    if game_id is None:
        return None

    return game_id[0]


from . import views
from . import messages
