import graphene

from graphene_sqlalchemy import SQLAlchemyObjectType
from model import Store as StoreModel

class Store(SQLAlchemyObjectType):
    class Meta:
        model = StoreModel

class Query(graphene.ObjectType):
    stores = graphene.List(Store)
    # stores = graphene.Field(
    #     Store, 
    #     id=graphene.Int(),
    #     name=graphene.String())

    def resolve_stores(self, name):
        query = Store.get_query(name)
        return query.all()

    # def resolve_stores(self, args, context, info):
    #     print(args, context, info)
    #     query = Store.get_query(context)
    #     query = query.filter_by(**args)
    #     return query.first()

schema = graphene.Schema(query=Query)