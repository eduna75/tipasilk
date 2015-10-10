__author__ = 'justus'

from app import app
from flask import render_template, request, url_for, redirect, send_from_directory


@app.route('/')
def index():
    return render_template('ouch-pack/index.html')


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])