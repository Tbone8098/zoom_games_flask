from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models.balderdash import model_player

DATABASE_SCHEMA = 'balderdash_db'

class Game:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.code = data['code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO games (name, code) VALUES (%(name)s, %(code)s)'
        new_games_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

        return new_games_id
    
# R !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM games;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if len(results) > 0:
            all_games = []
            for games in results:
                all_games.append(cls(games))
            return all_games

    @classmethod
    def get_one(cls, name_id):
        query = 'SELECT * FROM games WHERE id = %(name_id)s;'
        data = {
            'name_id': name_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return results

    @classmethod
    def get_one_by_code(cls, data):
        query = 'SELECT * FROM games WHERE code = %(game_code)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return results

    @classmethod
    def does_game_exist(cls, data):
        """data keys = code"""
        query = 'SELECT * from games WHERE code = %(code)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if results == False:
            return False
        elif len(results) == 0:
            return results
        return cls(results[0])

    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE games SET name=%(name)s WHERE id=%(name_id)s'
        data = {
            'first_name': info['first_name'],
            'name_id': info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, data):
        '''data = {"game_id": id}'''
        query = 'DELETE FROM games WHERE id=%(game_id)s'
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id

    @classmethod
    def delete_all(cls):
        query = 'DELETE FROM games'
        connectToMySQL(DATABASE_SCHEMA).query_db(query)

# Validations for Games
    @staticmethod
    def validate_create_game(data):
        """data keys = game_name, game_code"""
        is_valid = True
        if len(data['game_name']) < 2: 
            is_valid = False
            flash('Game name must be greater than 2 characters', 'game_name')
        
        if len(data['game_code']) < 7: 
            is_valid = False
            flash('Game Code must be greater than 3 characters', 'game_code')


        does_game_exist = Game.does_game_exist({
            'code': data['game_code']
        })

        if does_game_exist:
            is_valid = False
            flash("Game already exists")
        
        return is_valid

    @staticmethod
    def validate_join_game(data):
        """data keys = game_code, username"""

        print("*"*80)
        print(data)

        is_valid = True
        
        if len(data['game_code']) < 7:
            is_valid = False
            flash("Code must be greater than 7 characters")
        
        if len(data['username']) < 2:
            is_valid = False
            flash("Username must be greater than 2 characters")
        
        does_game_exist = Game.does_game_exist({
            'code': data['game_code']
        })

        if not does_game_exist:
            is_valid = False
            flash("Game does not exist")
        
        elif does_game_exist:
            all_players = model_player.Player.get_all_in_game({
                'game_id': does_game_exist.id
            })
            for player in all_players:
                if player.username == data['username']:
                    is_valid = False
                    flash("Username is already taken")
        
        return is_valid

