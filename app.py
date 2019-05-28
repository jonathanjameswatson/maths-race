import eventlet
from mathsrace import create_app, socketio

eventlet.monkey_patch()

app = create_app()

if __name__ == '__main__':
    socketio.run(app)
