from app import db

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    products = db.relationship("ProductInStore", back_populates="store", lazy="dynamic")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

    stores = db.relationship("ProductInStore", back_populates="product", lazy="dynamic")

class ProductInStore(db.Model):
    store_id = db.Column(db.Integer, db.ForeignKey(Store.id), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), primary_key=True)

    store = db.relationship("Store", back_populates="products")
    product = db.relationship("Product", back_populates="stores")
    
    quantity = db.Column(db.Integer)

