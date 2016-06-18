from flask_script import Manager, Server, Shell, prompt_pass
from flask_materialize_mongodb_blog import app
from flask_materialize_mongodb_blog.admin import AdminUser, User
from flask_materialize_mongodb_blog.blog import Category, Post, Tag


def _make_context():
    return dict(app=app, AdminUser=AdminUser, User=User,
                Category=Category, Post=Post, Tag=Tag)

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='5000',
                                        use_debugger=True))
manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def superuser():
    """Create a superuser.
       Default account is admin@test.com, password is admin."""
    email = prompt_pass("Input your email.(Default is admin@test.com)",
                        default='admin@test.com')
    password = prompt_pass("Input your passwod.(Default is admin)",
                           default='admin')
    user = AdminUser.objects(email=email).first()
    if user is None:
        user = AdminUser(email=email, username='admin', password=password)
        user.save()
        print('Create successful')
    else:
        print('Fail to create, maybe create a another new one?')

if __name__ == '__main__':

    manager.run()
