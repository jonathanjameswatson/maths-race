from flask import g
from flask_socketio import join_room, emit

from mathsrace.extensions import socketio
from mathsrace.blueprints.auth import load_logged_in_user
from ..game import init_game, add_to_user_game, leave_game, find_game


def update(players):
    socketio.emit('update', players, broadcast=True)


@socketio.on('connect')
def handle_message():
    load_logged_in_user()

    print(g.user['username'] + ' connected.')


@socketio.on('m_new_game')
def m_new_game():
    load_logged_in_user()

    user = g.user

    game_id = init_game(10, user['id'])
    players = add_to_user_game(user['id'], game_id)
    join_room(game_id)

    emit('joined_game', players)


@socketio.on('m_join_game')
def m_join_game(host_name):
    load_logged_in_user()

    user = g.user

    game_id = find_game(host_name)

    if game_id is None:
        emit('overlay_error', 'There is no game with a host with that name.')
        return None

    players = add_to_user_game(user['id'], game_id)
    join_room(game_id)

    emit('joined_game', players)
    emit('user_joined', user['username'], room=game_id, include_self=False)


@socketio.on('disconnect')
@socketio.on('m_user_leaving')
def user_leaving():
    load_logged_in_user()

    leave_game(g.user['id'])
