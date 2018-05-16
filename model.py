from app import db

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    products = db.relationship("Product", backref="store", lazy="dynamic")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    