__author__ = 'justus'

from app import app, db
from flask import render_template, request, url_for, redirect, session, jsonify, send_file, Blueprint, g
from app.admin.models import Emails, Blog, Images, Products, Categories, Faq, Users
from app.decorators import requires_login
from io import BytesIO
from werkzeug.security import check_password_hash
import base64
import StringIO
from datetime import timedelta
from PIL import Image


mod = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


@app.before_request
def before_request():
    g.posts = Blog.query.all()
    g.thumbnail = Images.query.all()
    g.user = None
    if 'user_id' in session:
        g.user = Users.query.get(session['user_id'])


# Admin related content
@mod.route('/')
@requires_login
def admin():
    admin_menu = app.config['ADMIN_MENU']  # will show more or less options depending on development / production
    email = Emails.query.filter_by(status=0).count()
    return render_template('admin/index.html', emails=email, admin_menu=admin_menu)


@mod.route('/create-blog', methods=['POST', 'GET'])
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

        return redirect(url_for('admin.admin', _anchor='/create-blog'))
    return render_template('admin/tipasilk/create-blog.html')


@mod.route('/update-blog', methods=['GET', 'POST'])
def update_blog():
    if request.method == 'POST':
        posts = Blog.query.get(request.form['post_id'])
        posts.title = request.form['title']
        posts.body = request.form['body']
        db.session.commit()
        return redirect(url_for('admin.admin', _anchor='/update-blog'))
    else:
        data = Blog.query.all()
        return render_template('admin/tipasilk/update-blog.html', data=data)


@mod.route('/delete-blog', methods=['POST', 'GET'])
def delete_blog():
    print request.form
    if request.method == 'POST':
        db.session.delete(Blog.query.get(request.form['post_id']))
        db.session.commit()

    return redirect(url_for('admin.admin', _anchor='/update-blog'))


@mod.route('/orders')
def orders():
    return render_template('admin/tipasilk/orders.html')


@mod.route('/products')
def products():
    product = Products.query.all()
    return render_template('admin/tipasilk/products.html', product=product)


@mod.route('/create-product', methods=['GET', 'POST'])
def create_product():
    product_list = Products.query.all()
    category = Categories.query.all()
    if request.method == 'POST':
        try:
            prod_name = request.form['name']
            prod = Products(product_nr=request.form['product_nr'], name=request.form['name'],
                            shortdesc=request.form['shortdesc'], longdesc=request.form['longdesc'],
                            price=request.form['price'], category_id=request.form['category'])
            db.session.add(prod)
            db.session.commit()
            if request.files:
                product_image = base64.b64encode(request.files['imageInput'].stream.read())

                thumbnail = resize_image(request.files['imageInput'])
                thumbnail = base64.b64encode(thumbnail)
                prod_id = [prod.id for prod in Products.query.filter_by(name=prod_name)]
                db.session.add(Images(image=product_image, product_id=prod_id[0], thumbnail=thumbnail))
                db.session.commit()
            return redirect(url_for('admin.admin', _anchor='/create-product'))
        except BaseException as e:
            print e, ' Something didn\'t worked that well'
            return redirect(url_for('admin.admin', _anchor='/create-product'))
    return render_template('admin/tipasilk/create-products.html', product=product_list, category=category)


@mod.route('/update-product', methods=['GET', 'POST'])
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
        return redirect(url_for('admin.admin', _anchor='update-product'))
    else:
        data = Products.query.all()
    return render_template('admin/tipasilk/update-product.html', data=data)


@mod.route('/delete-product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        product_data = Products.query.get(request.form['product_id'])
        db.session.delete(product_data)
        db.session.commit()
    return redirect(url_for('admin', _anchor='update-product'))


@mod.route('/add-image', methods=['GET', 'POST'])
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


@mod.route('/delete-image', methods=['GET', 'POST'])
def delete_image():
    if request.method == "POST":
        page = request.form['page']
        if request.form['delete']:
            db.session.delete(Images.query.get(request.form['image_id']))
            db.session.commit()
    return redirect(url_for('admin', _anchor=page))


@mod.route('/settings')
def settings():
    return render_template('admin/tipasilk/settings.html')


@mod.route('/emails')
def emails():
    email = Emails.query.all()
    return render_template('admin/tipasilk/emails.html', email=email)


@mod.route('/edit-faq', methods=['POST', 'GET'])
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
@mod.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session.permanent = True
            admin.permanent_session_lifetime = timedelta(minutes=10)
            session['user_id'] = user.id
        return redirect(url_for('admin.admin'))
    return render_template('admin/login.html')


@mod.route('/logout')
def logout():
    if session:
        session.pop('user_id', None)
        session.clear()
        return redirect(url_for('index'))


# not a view but a function
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


# AJAX response to load image in product page
@mod.route('/load-image')
def load_image():
    a = request.args.get('a', 0, type=str)
    a = int(a.replace('thumbnail-', ''))
    image = Images.query.get(a)
    image = image.image
    return jsonify(result=image)


@mod.route('/image/<size>/<int:img_id>.jpg')
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


@mod.route('/add-category')
def add_category():
    a = request.args.get('a', 0, type=str)
    db.session.add(Categories(name=a))
    db.session.commit()
    cat = Categories.query.all()
    result = []
    for c in cat:
        result.append((c.id, c.name))
    print result
    return jsonify(result=result)


@mod.errorhandler(400)
@mod.errorhandler(401)
@mod.errorhandler(402)
@mod.errorhandler(403)
@mod.errorhandler(404)
@mod.errorhandler(405)
@mod.errorhandler(406)
@mod.errorhandler(407)
@mod.errorhandler(408)
@mod.errorhandler(409)
@mod.errorhandler(410)
def error(e):
    return render_template('error.html', e=e), 404