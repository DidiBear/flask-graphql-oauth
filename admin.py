import sys, inspect
from flask import redirect, url_for, request
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user 

from app import app, db
from auth import User, OAuth

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

class NeedAdminRole:
    def is_accessible(self):
        admin_user = AdminUser.query.filter_by(user_id=current_user.get_id()).first()
        return admin_user is not None

class NeedAdminRoleIndexView(NeedAdminRole, AdminIndexView):
    pass

class NeedAdminRoleModelView(NeedAdminRole, ModelView):
    pass

admin = Admin(app, index_view=NeedAdminRoleIndexView(), template_mode='bootstrap3')

import model
app_models = dict(inspect.getmembers(model, inspect.isclass)).values()

for model in [AdminUser, User, OAuth] + list(app_models):
    admin.add_view(NeedAdminRoleModelView(model, db.session))
