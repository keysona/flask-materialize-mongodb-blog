from flask import Blueprint, render_template
from .models import *
from flask_materialize_mongodb_blog import app

blog = Blueprint('blog', __name__, template_folder='templates')


# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@blog.route('/', defaults={'page': 1})
@blog.route('/index/page/<int:page>')
def index(page):
    pagination = Post.objects.paginate(page=page, per_page=3)
    posts = pagination.items
    tags = Tag.objects.all()
    return render_template('index.html',
                           **{'posts': posts,
                              'pagination': pagination,
                              'tags': tags})


@blog.route('/post/<string:slug>')
def get_post_detail(slug):
    post = Post.objects.get_or_404(slug=slug)
    post.hit_count = post.hit_count + 1
    return render_template('post.html', post=post)


@blog.route('/categorys')
def show_category():
    categorys = Category.objects.all()


@blog.route('/category/<string:category>')
def get_category_detail():
    category = Category.objects.get_or_404()
