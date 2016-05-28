from flask.ext.script import Manager, Server
from flask_materialize_mongodb_blog import app


manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='5000',
                                        use_debugger=True))

if __name__ == '__main__':
    manager.run()
