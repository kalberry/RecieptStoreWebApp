from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    receipts = db.relationship('Receipt', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def loadUser(id):
        return User.query.get(int(id))

    def __repr__(self):
        return '<Customer email: {}>'.format(self.email)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(16))
    store = db.Column(db.String(64))
    sales_tax = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='receipt', lazy='dynamic')

    def __init__(self, date, store, sales_tax, subtotal, user_id):
        self.date = date
        self.store = store
        self.sales_tax = sales_tax
        self.subtotal = subtotal
        self.user_id = user_id

    def __repr__(self):
        return '<Receipt date {} - Store ID {}>'.format(self.date, self.store)

    def __eq__(self, other):
        if isinstance(other, Receipt):
            return self.date == other.date and\
                   self.store == other.store and\
                   self.subtotal == other.subtotal and\
                   self.sales_tax == other.sales_tax
        else:
            return other

    def __ne__(self, other):
        return not self.__eq__(other)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    category1 = db.Column(db.String(64))
    category2 = db.Column(db.String(64))
    category3 = db.Column(db.String(64))
    price = db.Column(db.Float)
    upc = db.Column(db.Integer)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __repr__(self):
        return '<Item {} - Price {}>'.format(self.name, self.price)

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.name == other.name and\
                   self.upc == other.upc
        else:
            return other

    def __ne__(self, other):
        return not self.__eq__(other)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_path = db.Column(db.String(128))
    file_name = db.Column(db.String(128))

    def in_db(self, url_path):
        return self.url_path == url_path

    def __repr__(self):
        return '<Image file path {} - Image URL path {}>'.format(self.filePath, self.url_path)
