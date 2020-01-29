from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Item, Receipt, Image
from app.forms import RegistrationForm, WalmartReceiptDataForm, LoginForm
from app.retailStore import add_image
from app.retailStore.walmart.api_call import api_call
from app.retailStore.walmart.get_categories import get_walmart_categories
from app.retailStore.walmart.store_data import store_walmart_data
from werkzeug.urls import url_parse
import json
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = WalmartReceiptDataForm()
    if form.validate_on_submit():
        receipt_data = api_call(form.store_id.data,
                                        form.purch_date.data,
                                        form.card_type.data,
                                        form.total.data,
                                        form.last_four.data)

        store_walmart_data(receipt_data, current_user.get_id())
        return redirect(url_for('viewreceipts'))
    return render_template('add.html', form=form)

@app.route('/viewreceipts')
@login_required
def viewreceipts():
    receipt_data = []
    user = User.query.filter_by(id=current_user.get_id()).first()
    receipt_list = user.receipts

    for receipt in receipt_list:
        receipt_items = []
        item_list = receipt.items

        for item in item_list:
            img = Image.query.filter_by(id=item.image_id).first()

            receipt_items.append({'image':img.file_name, 'name': item.name, 'category1':item.category1,
                'category2':item.category2, 'category3':item.category3, 'price':item.price,
                'upc':item.upc})

        if receipt_items is not None:
            receipt_data.append({'date':receipt.date, 'store':receipt.store, 'sales_tax':receipt.sales_tax,
                            'subtotal':receipt.subtotal, 'receipt_items':receipt_items})

    return render_template('viewreceipts.html', receipt_data=receipt_data) #, imgdir=imgdir)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        nextPage = request.args.get('next')
        if not nextPage or url_parse(nextPage).netloc != '':
            nextPage = url_for('index')
        return redirect(nextPage)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/itemImages/<path:file_name>')
def itemImage(file_name):
    file_name += '.jpg'
    return send_from_directory(app.config['IMG_DIR'], file_name)
