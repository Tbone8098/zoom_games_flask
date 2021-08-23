from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.balderdash import model_balderdash

@app.route('/balderdash')
def balderdash_index():
    session['page'] = 'balderdash_index'
    session['game'] = 'balderdash'
    return render_template('balderdash/index.html')

@app.route('/balderdash/game/create', methods=['POST'])
def create_game():
    # # check if game code 
    # is_valid = model_balderdash.Game.validate_games({
    #     'game_name': request.form['name'],
    #     'game_code': request.form['code']
    # })
    # if not is_valid:
    #     return redirect('/balderdash')
    # create game in db
    game_id = model_balderdash.Game.create({
        'name': request.form['name'],
        'code': request.form['code']
    })
    
    player_id = model_balderdash.Player.create({
        'username': request.form['username'],
        'game_id': game_id
        })

    session['game_code'] = request.form['code']
    session['uuid'] = player_id

    return redirect(f'/balderdash/{game_id}')

@app.route('/balderdash/game/join', methods=['POST'])
def join_game():
    # get game
    game = model_balderdash.Game.get_one_by_code({'code': request.form['code']})
    if not game:
        return redirect('/balderdash')

    player_id = model_balderdash.Player.create({
        'username': request.form['username'],
        'game_id': game.id
    })

    session['game_code'] = game.code
    session['uuid'] = player_id

    return redirect(f'/balderdash/{game.id}')

@app.route('/balderdash/game/<int:game_id>')
def game_page(game_id):
    # get game info
    game = model_balderdash.Game.get_one(game_id)
    if game.code != session['game_code']:
        return redirect('/balderdash')

    context = {
        'game': game,
        'all_players': model_balderdash.Player.get_all_in_game({
            'game_id': game.id
        })
    }

    return render_template('/balderdash/game/game_page.html', **context)

@app.route('/balderdash/<int:game_id>/delete')
def delete_game(game_id):
    all_players = model_balderdash.Player.get_all_in_game({
        'game_id': game_id
    })
    for player in all_players:
        model_balderdash.Player.delete_one({
            'id': player.id
        })
    model_balderdash.Game.delete_one({'id': game_id})
    return redirect('/balderdash')