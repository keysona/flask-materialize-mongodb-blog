import datetime
import logging
import flask_login as login

from flask import flash, request, redirect, url_for, render_template
from flask_admin.babel import gettext
from flask_admin.base import AdminIndexView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.contrib.mongoengine.helpers import format_error
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from .tools import markdown, format_datetime
from .forms import LoginForm

log = logging.getLogger("flask-admin.mongo")


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
                tag.count = len(tag.posts)
                tag.save()

    def on_model_delete(self, model):
        # remove this post to all tag.posts list
        tags = model.tags
        for tag in tags:
            if model in tag.posts:
                tag.posts.remove(model)
                tag.count = len(tag.posts)
                tag.save()

    def update_model(self, form, model):
        try:
            article_text = model['article_text']
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            if article_text != model['article_text']:
                model['modified_date'] = datetime.datetime.now()
                model['article_html'] = markdown(model['article_text'],
                                                 extras=['pyshell', 'fenced-code-blocks', 'link-with-blank'])  # cuddled-lists'
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

    def is_accessible(self):
        return login.current_user.is_authenticated


class TagView(ModelView):

    def _on_model_change(self, form, model, is_created):
        if is_created:
            model.save()
        category = model.category
        if model not in category.tags:
            category.tags.append(model)
            category.count = len(category.tags)
            category.save()

    def on_model_delete(self, model):
        category = model.category
        if model in category.tags:
            category.tags.remove(model)
            category.count = len(category.tags)
            category.save()

    def is_accessible(self):
        return login.current_user.is_authenticated


class CategoryView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


class AdminHomeView(AdminIndexView):

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super().index()

    @expose('/login', methods=('GET', 'POST'))
    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = form.get_user()
            login.login_user(user)
            return redirect(url_for('.index'))
        return render_template('form.html', form=form)

    @expose('/logout', methods=('GET', 'POST'))
    def logout(self):
        login.logout_user()
        return redirect(url_for('.index'))
