__author__ = 'justus'
__created__ = '29-01-2016'
__copyright__ = 'copyright @ Justus Ouwerling'

from app import app, db
from flask import render_template, request, send_from_directory, g, redirect, url_for
from app.admin.models import Blog, Products, Images
import base64

template = 'official/'


@app.before_request
def before_request():
    g.posts = Blog.query.all()


@app.route('/')
def index():
    return render_template(template + 'index.html')


@app.route('/blog')
def blog():
    return render_template(template + 'blog.html')


@app.route('/post/<int:post_id>')
def post(post_id=None):
    posts = Blog.query.filter_by(id=post_id).first()
    return render_template(template + 'post.html', post=posts)


@app.route('/about')
def about():
    return render_template(template + 'about.html')


@app.route('/contact')
def contact():
    return render_template(template + 'contact.html')


@app.route('/product')
def product():
    data = Products.query.all()
    return render_template(template + 'product.html', products=data)


@app.route('/product-spec/<int:prod_id>')
def product_spec(prod_id=None):
    data = Products.query.filter_by(id=prod_id)

    return render_template(template + 'product-single.html', data=data)


@app.route('/faq')
def faq():
    return render_template(template + 'faq.html')


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


# google site verification
@app.route('/google91fe3a6d5fb60907.html')
def google():
    return send_from_directory(app.static_folder, request.path[1:])


# Admin related content
@app.route('/admin')
def admin():
    return render_template('admin/index.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        post = Blog(request.form['title'], request.form['body'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('create'))
    return render_template(template + 'listview.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    posts = Blog.query.get(request.form['id'])
    if request.method == 'POST':
        posts.title = request.form['title']
        posts.body = request.form['body']
        db.session.commit()

    return redirect(url_for('create'))


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        db.session.delete(Blog.query.get(request.form['delete']))
        db.session.commit()

    return redirect(url_for('create'))


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    product_list = Products.query.all()
    if request.method == 'POST':
        try:
            prod = Products(request.form['product_nr'], request.form['name'], request.form['shortdesc'],
                            request.form['longdesc'], request.form['price'])
            db.session.add(prod)
            db.session.commit()
            return redirect(url_for('add_product'))
        except BaseException as e:
            print e
    return render_template(template + 'add-product.html', product=product_list)


@app.route('/delete-product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        db.session.delete(Products.query.get(request.form['delete']))
        db.session.commit()

    return redirect(url_for('add_product'))


@app.route('/add-image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        data = request.files['imageInput']
        data = base64.b64encode(data.stream.read())
        db.session.add(Images(data, request.form['productId']))
        db.session.commit()
    return redirect(url_for('add_product'))


@app.route('/delete-image', methods=['GET', 'POST'])
def delete_test():
    if request.method == "POST":
        if request.form['delete']:
            db.session.delete(Images.query.get(request.form['delete']))
            db.session.commit()
    return redirect(url_for('test'))