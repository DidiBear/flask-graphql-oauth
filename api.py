from flask import redirect
from flask_graphql import GraphQLView
from flask_login import login_required

from schema import schema
from config import DEBUG
from app import app

graphql_view = login_required(GraphQLView.as_view(name="graphql", schema=schema, graphiql=DEBUG, pretty=True))
app.add_url_rule('/graphql', view_func=graphql_view)

# @app.errorhandler(404)
# def page_not_found(e):
#     return redirect("graphql")
