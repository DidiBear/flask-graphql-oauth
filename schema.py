import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from model import Store as StoreModel, Product as ProductModel, Element as ElementModel, Capacity as CapacityModel

class Element(SQLAlchemyObjectType, interfaces=[relay.Node]):
    class Meta:
        model = ElementModel

class Product(SQLAlchemyObjectType, interfaces=[relay.Node]):
    class Meta:
        model = ProductModel

class Store(SQLAlchemyObjectType, interfaces=[relay.Node]):
    class Meta:
        model = StoreModel

class Capacity(SQLAlchemyObjectType, interfaces=[relay.Node]):
    class Meta:
        model = CapacityModel

    def resolve_type(self, info):
        return self.type.value

class Query(graphene.ObjectType):
    stores = SQLAlchemyConnectionField(Store)
    products = SQLAlchemyConnectionField(Product)
    # store = graphene.Field(Store)

    # def resolve_stores(self, info):
    #     # print(dir(info))
    #     return StoreModel.query.all()

    # def resolve_products(self, info):
    #     return ProductModel.query.all()

    # node = relay.Node.Field()
    # all_stores = SQLAlchemyConnectionField(Store)
    # all_products = SQLAlchemyConnectionField(Product)


# class Query(graphene.ObjectType):
#     store = graphene.List(graphene.String)

#     def resolve_hello(self, info):
#         print(info)
#         return ['Hello ca va', "mdr"]

schema = graphene.Schema(query=Query, types=[Store, Product, Element, Capacity]) 
