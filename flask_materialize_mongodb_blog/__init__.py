import yaml
from flask import Flask
from flask_mongoengine import MongoEngine


def create_app(setting_path=None):
    app = Flask(__name__, static_folder='./static/static')
    if setting_path is None:
        import os
        setting_path = os.path.join(os.path.dirname(__file__), 'setting.yaml')
    with open(setting_path) as f:
        setting = yaml.safe_load(f.read())
        app.config.update(setting['config'])
    return app


def register_blueprints(app):
    from .blog import blog
    app.register_blueprint(blog)


def register_admin(app):
    from .admin import create_admin, init_login
    admin = create_admin(name='blog', template_mode='bootstrap3')
    admin.init_app(app)
    init_login(app)


def register_filters(app):
    from .tools import format_datetime, my_truncate
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['my_truncate'] = my_truncate

app = create_app()
db = MongoEngine(app)

# register
register_blueprints(app)
register_admin(app)
register_filters(app)

if __name__ == '__main__':
    app.run()
