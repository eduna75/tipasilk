__author__ = 'justus'
__created__ = '29-01-2016'
__copyright__ = 'copyright @ Justus Ouwerling'

from app import app, db
from flask import render_template, request, send_from_directory, g, redirect, url_for, session, flash, jsonify
from app.admin.models import Blog, Products, Images, Faq, Users, Emails
from app.decorators import requires_login
from werkzeug.security import check_password_hash
import base64
from PIL import Image
import StringIO
from datetime import timedelta


template = 'official/'


@app.before_request
def before_request():
    g.posts = Blog.query.all()
    g.thumbnail = Images.query.all()
    g.user = None
    if 'user_id' in session:
        g.user = Users.query.get(session['user_id'])


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


# Admin related content
@app.route('/admin')
@requires_login
def admin():
    email = Emails.query.filter_by(status=0).count()
    return render_template('admin/index.html', emails=email)


@app.route('/create-blog', methods=['POST', 'GET'])
def create_blog():
    if request.method == 'POST':
        post_title = request.form['title']
        data = request.files['imageInput']
        data = base64.b64encode(data.stream.read())
        posts = Blog(title=request.form['title'], body=request.form['body'])
        db.session.add(posts)
        db.session.commit()
        if request.files:
            blog_id = [post.id for post in Blog.query.filter_by(title=post_title)]
            image = Images(image=data, blog_id=blog_id[0], thumbnail='')
            db.session.add(image)
            db.session.commit()

        return redirect(url_for('admin', _anchor='/create-blog'))
    return render_template('admin/tipasilk/create-blog.html')


@app.route('/update-blog', methods=['GET', 'POST'])
def update_blog():
    if request.method == 'POST':
        posts = Blog.query.get(request.form['post_id'])
        posts.title = request.form['title']
        posts.body = request.form['body']
        db.session.commit()
        return redirect(url_for('admin', _anchor='/update-blog'))
    else:
        data = Blog.query.all()
        return render_template('admin/tipasilk/update-blog.html', data=data)


@app.route('/delete-blog', methods=['POST', 'GET'])
def delete_blog():
    print request.form
    if request.method == 'POST':
        db.session.delete(Blog.query.get(request.form['post_id']))
        db.session.commit()

    return redirect(url_for('admin', _anchor='/update-blog'))


@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    product_list = Products.query.all()
    if request.method == 'POST':
        try:
            prod_name = request.form['name']
            prod = Products(product_nr=request.form['product_nr'], name=request.form['name'],
                            shortdesc=request.form['shortdesc'], longdesc=request.form['longdesc'],
                            price=request.form['price'])
            db.session.add(prod)
            db.session.commit()
            if request.files:
                product_image = base64.b64encode(request.files['imageInput'].stream.read())

                thumbnail = resize_image(request.files['imageInput'])
                thumbnail = base64.b64encode(thumbnail)
                prod_id = [prod.id for prod in Products.query.filter_by(name=prod_name)]
                db.session.add(Images(image=product_image, product_id=prod_id[0], thumbnail=thumbnail))
                db.session.commit()
            return redirect(url_for('admin', _anchor='/create-product'))
        except BaseException as e:
            print e, ' Something didn\'t worked that well'
            return redirect(url_for('admin', _anchor='/create-product'))
    return render_template('admin/tipasilk/create-products.html', product=product_list)


@app.route('/update-product', methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        try:
            product_data = Products.query.get(request.form['product_id'])
            product_data.product_nr = request.form['product_nr']
            product_data.name = request.form['name']
            product_data.shortdesc = request.form['shortdesc']
            product_data.longdesc = request.form['longdesc']
            product_data.price = request.form['price']
            db.session.add(product_data)
            db.session.commit()
        except BaseException as e:
            print e
        return redirect(url_for('admin', _anchor='update-product'))
    else:
        data = Products.query.all()
    return render_template('admin/tipasilk/update-product.html', data=data)


@app.route('/delete-product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_data = Products.query.get(request.form['product_id'])
        db.session.delete(product_data)
        db.session.commit()
    return redirect(url_for('admin', _anchor='update-product'))


@app.route('/add-image', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        page = request.form['page']

        image_data = request.files['imageInput']
        preprocessor = resize_image(image_data)
        image = base64.b64encode(preprocessor[0])

        thumbnail = base64.b64encode(preprocessor[1])
        db.session.add(Images(thumbnail=thumbnail, image=image, product_id=request.form['page_id']))
        db.session.commit()
    return redirect(url_for('admin', _anchor=page))


@app.route('/delete-image', methods=['GET', 'POST'])
def delete_image():
    if request.method == "POST":
        page = request.form['page']
        if request.form['delete']:
            db.session.delete(Images.query.get(request.form['image_id']))
            db.session.commit()
    return redirect(url_for('admin', _anchor=page))


@app.route('/settings')
def settings():
    return render_template('admin/tipasilk/settings.html')


@app.route('/emails')
def emails():
    email = Emails.query.all()
    return render_template('admin/tipasilk/emails.html', email=email)


@app.route('/edit-faq', methods=['POST', 'GET'])
def edit_faq():
    if request.method == 'POST':
        if 'add-faq' in request.form:
            faq_data = Faq(title=request.form['title'], body=request.form['body'], section=request.form['section'])
            db.session.add(faq_data)
            db.session.commit()
        elif 'delete-faq' in request.form:
            db.session.delete(Faq.query.get(request.form['delete-faq']))
            db.session.commit()
        return redirect(url_for('admin', _anchor='edit-faq'))
    faqs = Faq.query.all()
    return render_template('admin/tipasilk/edit-faq.html', faqs=faqs)


# login and logout
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=10)
            session['user_id'] = user.id
        return redirect(url_for('admin'))
    return render_template('admin/login.html')


@app.route('/logout')
def logout():
    if session:
        session.pop('user_id', None)
        session.clear()
        return redirect(url_for('index'))


# not a view but a function goes below
def resize_image(data):
    try:
        size = (450, 600)
        image = Image.open(data)
        image.thumbnail(size)
        result = StringIO.StringIO()
        image.save(result, format='JPEG')

        small_size = (150, 200)
        thumbnail = Image.open(data)
        thumbnail.thumbnail(small_size)
        result2 = StringIO.StringIO()
        thumbnail.save(result2, format='JPEG')

        reply = [result.getvalue(), result2.getvalue()]
    except BaseException as e:
        print e, ' resize image:'

    return reply


@app.route('/load-image')
def load_image():
    a = request.args.get('a', 0, type=str)
    a = int(a.replace('thumbnail-', ''))
    image = Images.query.get(a)
    image = image.image
    return jsonify(result=image)