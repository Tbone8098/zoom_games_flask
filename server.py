from flask_app import app, socketio
from flask_app.controllers import routes
from flask_app.controllers.balderdash import controller_game, controller_word, controller_socketio


if __name__ == '__main__':
    socketio.run(app)