from flask import Flask, redirect
from flask_graphql import GraphQLView

from config import HOSTNAME, PORT, DEBUG
from model import db
from schema import schema

app = Flask(__name__)

app.config['SECRET_KEY'] = 'itsatrap'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(name="graphql", schema=schema, graphiql=DEBUG, pretty=True))

@app.errorhandler(404)
def page_not_found(e):
    return redirect("graphql")

if __name__ == '__main__':
    app.run(HOSTNAME, port=PORT, debug=DEBUG)
