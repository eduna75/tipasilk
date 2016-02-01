__author__ = 'justus'
__created__ = '29-01-2016'
__copyright__ = 'copyright @ Justus Ouwerling'


from app import app
from flask import render_template, request, send_from_directory

template = 'official/'


@app.route('/')
def index():
    return render_template(template + 'index.html')


@app.route('/blog')
def blog():
    return render_template(template + 'blog.html')


@app.route('/about')
def about():
    return render_template(template + 'about.html')


@app.route('/contact')
def contact():
    return render_template(template + 'contact.html')


@app.route('/product')
def product():
    return render_template(template + 'product.html')


@app.route('/faq')
def faq():
    return render_template(template + 'faq.html')


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/google91fe3a6d5fb60907.html')
def google():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/admin-blog')
def admin_blog():
    return render_template(template + 'admin.html')