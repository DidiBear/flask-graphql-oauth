from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user 

from app import app, db
from model import Store, Product
from auth import User, OAuth

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

class NeedAdminRole:
    def is_accessible(self):
        admin_user = AdminUser.query.filter_by(user_id=current_user.get_id()).first()
        return admin_user is not None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class NeedAdminRoleIndexView(AdminIndexView, NeedAdminRole):
    pass

class NeedAdminRoleModelView(ModelView, NeedAdminRole):
    pass

admin = Admin(app, index_view=NeedAdminRoleIndexView(), template_mode='bootstrap3')

for model in [AdminUser, User, OAuth, Store, Product]:
    admin.add_view(NeedAdminRoleModelView(model, db.session))
