from flask_materialize_mongodb_blog import db


class User(db.Document):

    email = db.EmailField(required=True, unique=True)
    username = db.StringField(max_length=30, required=True)
    password = db.StringField(required=True)

    meta = {
            'allow_inheritance': True
        }

    def __unicode__(self):
        return '<%s> %s' % (self.email, self.username)


class AdminUser(User):

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
