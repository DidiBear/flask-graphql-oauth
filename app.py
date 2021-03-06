from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DEBUG

# Init project
app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from admin import *
from auth import *
from api import *

def main():
    import sys, os
    if "--reset" in sys.argv:
        os.remove("./database.db")
        with app.app_context():
            db.create_all()
            db.session.add(AdminUser(user_id=1))
            db.session.commit()
            print("Database tables created")
    else:
        app.run(debug=DEBUG)

if __name__ == "__main__":
    main()
