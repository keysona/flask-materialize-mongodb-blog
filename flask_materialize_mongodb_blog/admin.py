import datetime
import logging

from flask import flash
from flask.ext.admin.babel import gettext
from flask.ext.admin.contrib.mongoengine.helpers import format_error
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
import flask_login as login
from wtforms import TextAreaField, form, fields, validators
from wtforms.widgets import TextArea

from . import app
from .models import AdminUser
from .tools import markdown

log = logging.getLogger("flask-admin.mongo")


def format_datetime(view, context, model, name):
    datetime = model[name]
    return "%s年%s月%s日 %s:%s" % (datetime.year, datetime.month, datetime.day,
                                datetime.hour, datetime.second)


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PostView(ModelView):

    column_exclude_list = ['article_text', 'article_html', 'slug']
    column_formatters = {'created_date': format_datetime,
                         'modified_date': format_datetime}

    form_excluded_columns = ['article_html']

    form_overrides = {
        # 'article_text': CKTextAreaField
        }
    create_template = 'ckedit.html'
    edit_template = 'ckedit.html'

    def _on_model_change(self, form, model, is_created):

        if is_created:
            # convert markdown text to html
            model['article_html'] = markdown(model['article_text'],
                                             extras=['pyshell', 'fenced-code-blocks'])
            # first save document to get reference
            model.save()

        # add this post to all tags.post list.
        for tag in model.tags:
            if model not in tag.posts:
                tag.posts.append(model)
                tag.save()

    def on_model_delete(self, model):
        # remove this post to all tag.posts list
        tags = model.tags
        for tag in tags:
            if model in tag.posts:
                tag.posts.remove(model)
                tag.save()

    def update_model(self, form, model):
        try:
            article_text = model['article_text']
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            if article_text != model['article_text']:
                model['modified_date'] = datetime.datetime.now()
                model['article_html'] = markdown(model['article_text'], extras=['pyshell', 'fenced-code-blocks']) # cuddled-lists'
            model.save()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to update record. %(error)s',
                              error=format_error(ex)),
                      'error')
            log.exception('Failed to update record.')

            return False
        else:
            self.after_model_change(form, model, False)

        return True


class TagView(ModelView):
    def _on_model_change(self, form, model, is_created):
        if is_created:
            model.save()
        category = model.category
        if model not in category.tags:
            category.tags.append(model)
            category.save()

    def on_model_delete(self, model):
        category = model.category
        if model in category.tags:
            category.tags.remove(model)
            category.save()


class CategoryView(ModelView):
    pass


class LoginForm(form.Form):

    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):

        if self.login.data not in \
                [app.config['username'], app.config['email']]:
            raise validators.ValidationError('Invalid username or password!')

        if self.password.data != app.config['password']:
            raise validators.ValidationError('Invalid password!')


def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.Objects.get(id=user-id).first()


def create_admin(app, *args, **kwargs):

    return Admin(app, *args, **kwargs)
