import datetime
from flask import url_for
from . import db


class Category(db.Document):

    name = db.StringField(verbose_name='类别',
                          max_length=255,
                          required=True,
                          unique=True)

    tags = db.ListField(db.ReferenceField('Tag'))

    def __unicode__(self):
        return self.name


class Tag(db.Document):

    name = db.StringField(verbose_name='标签',
                          max_length=255,
                          required=True,
                          unique=True)

    category = db.ReferenceField(Category, verbose_name='目录')
    posts = db.ListField(db.ReferenceField('Post'))

    def __unicode__(self):
        return self.name


class Post(db.Document):

    created_date = db.DateTimeField(verbose_name='创建日期',
                                    default=datetime.datetime.now)

    modified_date = db.DateTimeField(verbose_name='修改日期',
                                     default=datetime.datetime.now)

    title = db.StringField(verbose_name='标题',
                           max_length=255, required=True)

    slug = db.StringField(verbose_name='url参数',
                          max_length=255,
                          required=True, unique=True)

    article_text = db.StringField(verbose_name='markdown文本', required=True)

    article_html = db.StringField(verbose_name='html文本')

    hit_count = db.LongField(verbose_name='点击次数', default=0)

    tags = db.ListField(db.ReferenceField(Tag,
                                          reverse_delete_rule=db.PULL), verbose_name='标签')

    category = db.ReferenceField(Category)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ['-created_date',
                    'slug',
                    '$article_html'],
        'ordering': ['-created_date']
        }


class User(db.Document):

    email = db.EmailField(required=True, unique=True)
    username = db.StringField(max_length='30', required=True)
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
