__author__ = 'justus'
__created__ = '29-01-2016'
__copyright__ = 'copyright @ Justus Ouwerling'

from app import app, db
from flask import render_template, request, send_from_directory, g, redirect, url_for, session, flash, jsonify, \
    send_file
from app.admin.models import Blog, Products, Images, Faq, Users, Emails, Categories
from app.decorators import requires_login
from werkzeug.security import check_password_hash
import base64
from PIL import Image
import StringIO
from datetime import timedelta
from io import BytesIO


template = 'official/'


@app.route('/')
def index():
    return render_template(template + 'index.html')


@app.route('/blog')
def blog():
    return render_template(template + 'blog.html')


@app.route('/post/<int:post_id>')
def post(post_id=None):
    posts = Blog.query.filter_by(id=post_id).first()
    return render_template(template + 'post.html', post=posts, session=session)


@app.route('/about')
def about():
    return render_template(template + 'about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print request.remote_addr
        email = Emails(name=request.form['name'], email=request.form['email'], body=request.form['body'],
                       senders_ip=request.remote_addr)
        db.session.add(email)
        db.session.commit()
        flash(u'Your message has been send, thank you and have a great day.!')
        return redirect(url_for('contact'))
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
    faqs = Faq.query.all()
    return render_template(template + 'faq.html', faqs=faqs)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


# google site verification
@app.route('/google91fe3a6d5fb60907.html')
def google():
    return send_from_directory(app.static_folder, request.path[1:])


# AJAX response to load image in product page
@app.route('/load-image')
def load_image():
    a = request.args.get('a', 0, type=str)
    a = int(a.replace('thumbnail-', ''))
    image = Images.query.get(a)
    image = image.image
    return jsonify(result=image)


@app.route('/image/<size>/<int:img_id>.jpg')
def image(size, img_id=None):
    img = Images.query.filter_by(id=img_id)
    th = []
    if 'thumbnail' in size:
        for i in img:
            th.append(i.thumbnail)
    elif 'image' in size:
        for i in img:
            th.append(i.image)
    byte_io = BytesIO()
    a = StringIO.StringIO(th[0].decode('base64'))
    i = Image.open(a)
    i.save(byte_io, 'JPEG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/jpeg')


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(402)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(406)
@app.errorhandler(407)
@app.errorhandler(408)
@app.errorhandler(409)
@app.errorhandler(410)
@app.errorhandler(500)
@app.errorhandler(501)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
def error(e):
    return render_template(template + 'error.html', e=e), 404