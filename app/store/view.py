__author__ = 'justus'

from flask import Blueprint, request, session, redirect, url_for, render_template
from app.admin.models import Products

mod = Blueprint('store', __name__, static_folder='static', url_prefix='/store')


@mod.route('/')
def index():
    return redirect(url_for('index'))


@mod.route('/cart', methods=['GET', 'POST'])
def cart():
    print session['cart']
    if request.method == 'POST':
        product = Products.query.get(request.form['product'])
        if 'cart' in session:
            if not any(product.name in d for d in session['cart']):
                session['cart'].append({product.name: [int(request.form['quantity']),
                                                       int(float(request.form['price'])),
                                                       product.product_nr,
                                                       product.id]})
            elif any(product.name in d for d in session['cart']):
                for d in session['cart']:
                    d.update((k, [int(request.form['quantity']), int(float(request.form['price'])), product.product_nr,
                             product.id]) for k, v in d.items() if k == product.name)
        else:
            session['cart'.format(id)] = [{product.name: [int(request.form['quantity']),
                                                          int(float(request.form['price'])),
                                                          product.product_nr,
                                                          product.id]}]
    return redirect(request.referrer)


@mod.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        if request.form['delete']:
            for d in session['cart']:
                d.pop(request.form['id'], None)
    return redirect(request.referrer)