__author__ = 'justus'

from flask import Blueprint, request, session, redirect, url_for
from app.admin.models import Products

mod = Blueprint('store', __name__, static_folder='static', url_prefix='/store')


@mod.route('/')
def index():
    return redirect(url_for('index'))


@mod.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product = Products.query.get(request.form['product'])
        if 'cart' in session:
            if not any(product.name in d for d in session['cart']):
                session['cart'].append({product.name: [int(request.form['quantity']), int(float(request.form['price']))]})
            elif any(product.name in d for d in session['cart']):
                for d in session['cart']:
                    d.update((k, [int(request.form['quantity']), int(float(request.form['price']))]) for k, v in d.items() if k == product.name)
        else:
            session['cart'.format(id)] = [{product.name: [int(request.form['quantity']), int(float(request.form['price']))]}]
        if 'delete' in request.form:
            pass
    return redirect(request.referrer)