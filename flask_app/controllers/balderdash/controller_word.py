from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
# from flask_app.models import 

@app.route('/balderdash/word/create')
def add_word():
    resp = {
        'code': 200,
        'msg': 'success'
    }
    return jsonify(resp)
