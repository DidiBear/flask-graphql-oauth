import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import sys
from flask import Flask, redirect, url_for, flash, render_template
from flask_graphql import GraphQLView
from config import HOSTNAME, PORT, DEBUG

from model import db
from schema import schema
from auth import auth_blueprint, login_manager, login_required, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'itsatrap'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.register_blueprint(auth_blueprint, url_prefix="/login")
app.add_url_rule('/graphql', view_func=login_required(GraphQLView.as_view(name="graphql", schema=schema, graphiql=DEBUG, pretty=True)))

@app.errorhandler(404)
def page_not_found(e):
    return redirect("graphql")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("home.html")

db.init_app(app)
login_manager.init_app(app)

if __name__ == "__main__":
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")
    else:
        app.run(debug=DEBUG)
