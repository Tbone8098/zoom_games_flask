from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models.balderdash import model_game

DATABASE_SCHEMA = 'balderdash_db'



class Player:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.score = data['score']
        self.game_id = data['game_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# C !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def create(cls, data):
        """data keys = username, game_id """
        query = 'INSERT INTO players (username, game_id) VALUES (%(username)s, %(game_id)s)'
        new_players_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_players_id
    
    # @classmethod
    # def join_one(cls, data)
    # """data keys = player_id, game_id"""
    # query = 'INSERT INTO round_has_players'

# R !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM players;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        if len(results) > 0:
            all_players = []
            for players in results:
                all_players.append(cls(players))
            return all_players

    @classmethod
    def get_all_in_game(cls, data):
        """data keys = game_id"""
        query = 'SELECT * FROM players WHERE game_id = %(game_id)s;'
       
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        all_players = []
        if len(results) > 0:
            for player in results:
                all_players.append(cls(player))
            return all_players
        return results
    
    @classmethod
    def get_one(cls, data):
        """data keys = player_id"""
        query = 'SELECT * FROM players WHERE id = %(player_id)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
           return cls(results[0])
        return results
    
# U !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def update_one(cls, info):
        # TODO: add the ability to update pw 
        query = 'UPDATE players SET username=%(username)s WHERE id=%(username_id)s'
        data = {
            'first_name': info['first_name'],
            'username_id': info['id'],
        }
        return connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# D !!!!!!!!!!!!!!!!!!!!!!!!
    @classmethod
    def delete_one(cls, data):
        """data keys = id"""
        query = 'DELETE FROM players WHERE id=%(id)s'
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)

# # Validations
#     @staticmethod
#     def validate_players(data):
#         """data keys = username, game_code"""
#         is_valid = True

#         if len(data['username']) < 3: 
#             is_valid = False
#             flash('username name must be greater than 3 characters')
#         else:
#             game = model_game.Game.does_game_exist(data['game_code'])
#             all_players = Player.get_all_in_game(game.id)
#             for player in all_players:
#                 if player.username == data['username']:
#                     is_valid = False
#                     flash("Username is already taken")
        
#         return is_valid