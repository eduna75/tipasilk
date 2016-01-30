__author__ = 'justus'
__created__ = '29-01-2016'
__copyright__ = 'copyright @ Justus Ouwerling'


from app import app
from flask import render_template, request, send_from_directory


@app.route('/')
def index():
    return render_template('official/index.html')


@app.route('/blog')
def blog():
    return render_template('official/base.html')


@app.route('/about')
def about():
    return render_template('official/about.html')


@app.route('/contact')
def contact():
    return 'contact'


@app.route('/product')
def product():
    return 'catalog'


@app.route('/faq')
def faq():
    return 'knowledge'


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])