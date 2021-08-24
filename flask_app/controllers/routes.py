from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'