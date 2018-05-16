import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import redirect, url_for, flash, render_template
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import (
    LoginManager, UserMixin, current_user,
    login_required, login_user, logout_user
)
from app import app, db, login_manager

auth_blueprint = make_github_blueprint(
    client_id="f75638c39c89011654bc",
    client_secret="cb9b1536546bc490c8c47f3ea3f779687815ac14",
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    # ... other columns as needed

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

# setup login manager
login_manager.login_view = 'github.login'

@app.route("/")
def index():
    return render_template("home.html")

app.register_blueprint(auth_blueprint, url_prefix="/login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# setup SQLAlchemy backend
auth_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(auth_blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with GitHub.", category="error")
        return False

    resp = blueprint.session.get("/user")
    if not resp.ok:
        msg = "Failed to fetch user info from GitHub."
        flash(msg, category="error")
        return False

    github_info = resp.json()
    github_user_id = str(github_info["id"])

    # Find this OAuth token in the database, or create it
    try:
        oauth = OAuth.query \
            .filter(OAuth.provider == blueprint.name) \
            .filter(OAuth.provider_user_id == github_user_id) \
            .one()

    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=github_user_id, token=token)


    if not oauth.user:
        # Create a new local user account for this user
        user = User(username=github_info["name"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
    
    # Log in the new local user account
    login_user(oauth.user)
    flash("Successfully signed in with GitHub.")

    return False # Disable Flask-Dance's default behavior for saving the OAuth token

# notify on OAuth provider error
@oauth_error.connect_via(auth_blueprint)
def github_error(blueprint, error, error_description=None, error_uri=None):
    msg = f"OAuth error from {blueprint.name}! error={error} description={error_description} uri={error_uri}"

    flash(msg, category="error")
