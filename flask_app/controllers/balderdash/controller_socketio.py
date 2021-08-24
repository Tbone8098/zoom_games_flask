from flask_app import app, socketio
from flask import render_template, redirect, request, session, flash, jsonify
from flask_socketio import send, emit
from flask_app.models.balderdash import model_game, model_player

@socketio.on('connected')
def connect(data):
    player = model_player.Player.get_one({
        'player_id': session['uuid']
    })
    data = {
        'msg': f'{player.username} has connected to the game',
        'player_info': {
            'username': player.username,
            'id': player.id,
            'game_id': player.game_id
        }
    }
    emit("connected_resp", data, broadcast=True)