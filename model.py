
import enum
from app import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # One to Many
    elements = db.relationship("Element", backref="store", cascade="all, delete-orphan", lazy="dynamic")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Many to one
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))

    # One to one
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", backref="elements")

    # One to one
    capacity_id = db.Column(db.Integer, db.ForeignKey("capacity.id"))
    capacity = db.relationship("Capacity", backref="elements")
    
    remaining = db.Column(db.Integer)

class Capacity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    type = db.Column(db.String)
