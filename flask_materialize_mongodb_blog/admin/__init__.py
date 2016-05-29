import flask_login as login
from flask_admin import Admin

from .views import PostView, TagView, CategoryView, AdminHomeView
from .models import AdminUser, User
from flask_materialize_mongodb_blog.blog.models import Post, Tag, Category


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.objects(id=user_id).first()


def create_admin(*args, **kwargs):
    admin = Admin(index_view=AdminHomeView(endpoint='admin'), *args, **kwargs)
    admin.add_view(PostView(Post))
    admin.add_view(TagView(Tag))
    admin.add_view(CategoryView(Category))
    return admin


def create_admin_blueprint(admin):
    from flask_admin.base import create_blueprint
    admin_blueprint = create_blueprint(admin)
    return admin_blueprint
