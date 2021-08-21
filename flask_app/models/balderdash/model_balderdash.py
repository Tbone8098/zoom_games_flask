from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

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
        one_games = []
        if len(results) > 0:
           return cls(results[0])
        return results

    @classmethod
    def get_one_by_code(cls, data):
        query = 'SELECT * from games WHERE code = %(code)s;'
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return False

    
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
        '''data = {"id": id}'''
        query = 'DELETE FROM games WHERE id=%(id)s'
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id

# Validations for Games
    @staticmethod
    def validate_games(user_data):
        is_valid = True

        if len(user_data['name']) < 3: 
            is_valid = False
            flash('name name must be greater than 3 characters')
        
        return is_valid



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
    def get_one(cls, username_id):
        query = 'SELECT * FROM players WHERE id = %(username_id)s;'
        data = {
            'username_id': username_id
        }
        results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        one_players = []
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
    def delete_one(cls, username_id):
        query = 'DELETE FROM players WHERE id=%(username_id)s'
        data = {
            'usernameid': username_id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query,data)
        return id


# ******************************************* VALIDATIONS ********************************************
    @staticmethod
    def validate_players(user_data):
        is_valid = True

        if len(user_data['username']) < 3: 
            is_valid = False
            flash('username name must be greater than 3 characters')
        
        return is_valid