__author__ = 'justus'

from app import app
from flask import render_template, request, url_for, redirect


@app.route('/')
def index():
    return render_template('ouch-pack/index.html')