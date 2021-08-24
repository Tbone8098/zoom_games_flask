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

@socketio.on("leave_game")
def leave_game():
    player = model_player.Player.get_one({
        'player_id': session['uuid']
    })
    print(f"{player.username} is leaving the game")

    all_players = model_player.Player.get_all_in_game({
        'game_id': session['game_id']
    })

    data = {
        'username': player.username
    }

    if len(all_players) == 1:
        model_game.Game.delete_one({
            'game_id': session['game_id']
        })
        print("Game deleted")
    
    model_player.Player.delete_one({'id': session['uuid']})

    emit("leave_game_resp")
    emit("leave_game_resp_broadcast", data, broadcast=True)