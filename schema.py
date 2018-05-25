import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from model import Store as StoreModel, Product as ProductModel, Element as ElementModel, Capacity as CapacityModel

# interfaces=[relay.Node]
class Element(SQLAlchemyObjectType):
    class Meta:
        model = ElementModel

class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel

class Store(SQLAlchemyObjectType):
    class Meta:
        model = StoreModel

class Capacity(SQLAlchemyObjectType):
    class Meta:
        model = CapacityModel

class Query(graphene.ObjectType):
    # stores = SQLAlchemyConnectionField(Store)
    # products = SQLAlchemyConnectionField(Product)
    stores = graphene.List(Store)
    products = graphene.List(Product)

    def resolve_stores(self, info):
        return StoreModel.query.all()

    def resolve_products(self, info):
        return ProductModel.query.all()

    # node = relay.Node.Field()
    # all_stores = SQLAlchemyConnectionField(Store)
    # all_products = SQLAlchemyConnectionField(Product)

# class CreateProduct(SQLAlchemyMutation):
#     class Input:
#         model = ProductModel
#         field = Product


# class Mutation(graphene.ObjectType):
#     create_product = CreateProduct.Field()


schema = graphene.Schema(query=Query, types=[Store, Product, Element, Capacity]) 
