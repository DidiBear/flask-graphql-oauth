import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from flask import redirect, url_for, flash, render_template
from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import (
    LoginManager, UserMixin, current_user,
    login_required, login_user, logout_user
)
from app import app, db, login_manager

auth_github_blueprint = make_github_blueprint(
    client_id="f75638c39c89011654bc",
    client_secret="cb9b1536546bc490c8c47f3ea3f779687815ac14",)

auth_google_blueprint = make_google_blueprint(
    client_id="976500073047-ut7hra9br3ieu2ah1pu5er499s09j42i.apps.googleusercontent.com",
    client_secret="ZddX-0tLEGczrn45gwAYaOMc",
    scope=["profile", "email"])

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    # ... other columns as needed

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

# setup login manager
# login_manager.login_view = 'github.login'
login_manager.login_view = 'google.login'

@app.route("/")
def index():
    return render_template("home.html")

app.register_blueprint(auth_google_blueprint, url_prefix="/login")
app.register_blueprint(auth_github_blueprint, url_prefix="/login")

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
auth_github_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
auth_google_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(auth_github_blueprint)
def github_logged_in(blueprint, token):
    return oauth_logged_in(blueprint.name, token, 
        get_response=lambda: blueprint.session.get("/user"),
        get_info=lambda info: (info["id"], info["name"]))

@oauth_authorized.connect_via(auth_google_blueprint)
def google_logged_in(blueprint, token):
    return oauth_logged_in(blueprint.name, token, 
        get_response=lambda: google.get("/plus/v1/people/me"),
        get_info=lambda info: (info["id"], info["displayName"]))

def oauth_logged_in(provider, token, get_response, get_info):
    if not token:
        flash(f"Failed to log in with {provider}.", category="error")
        return False

    resp = get_response()
    if not resp.ok or not resp.text:
        flash(f"Failed to fetch user info from {provider}.", category="error")
        return False

    user_id, username = get_info(resp.json())

    # Find this OAuth token in the database, or create it
    try:
        oauth = OAuth.query \
            .filter(OAuth.provider == provider) \
            .filter(OAuth.provider_user_id == user_id) \
            .one()

    except NoResultFound:
        oauth = OAuth(provider=provider, provider_user_id=user_id, token=token)


    if not oauth.user:
        # Create a new local user account for this user
        # google["emails"][0]["value"]
        user = User(username=username)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
    
    # Log in the new local user account
    login_user(oauth.user)
    flash(f"Successfully signed in with {provider}.")

    return False # Disable Flask-Dance's default behavior for saving the OAuth token

# notify on OAuth provider error
@oauth_error.connect_via(auth_github_blueprint)
def github_error(blueprint, error, error_description=None, error_uri=None):
    msg = f"OAuth error from {blueprint.name}! error={error} description={error_description} uri={error_uri}"

    flash(msg, category="error")

@oauth_error.connect_via(auth_google_blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = f"OAuth error from {blueprint.name}! error={error} description={error_description} uri={error_uri}"

    flash(msg, category="error")
