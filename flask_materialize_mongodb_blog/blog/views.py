from flask import Blueprint, render_template, request
from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed
from .models import *
from flask_materialize_mongodb_blog import app


blog = Blueprint('blog', __name__, template_folder='templates')


# error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def make_external(slug):
    return urljoin(request.url_root, url_for('blog.get_post_detail',
                                             slug=slug))


@blog.route('/recent.atom')
def recent_feed():
    print(request.url, request.url_root)
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    for post in Post.objects[:10]:
        feed.add(post.title, post.article_html,
                 content_type='html', author=app.config['author'],
                 url=make_external(post.slug),
                 updated=post.modified_date,
                 published=post.created_date)
        return feed.get_response()


@blog.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages


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

# category
@blog.route('/categorys')
def show_category():
    categorys = Category.objects.all()


@blog.route('/category/<string:category>')
def get_category_detail():
    category = Category.objects.get_or_404()


# tag
@blog.route('/tag/<string:name>')
def get_tag_detail(name):
    tag = Tag.objects.get_or_404(name=name)
    return render_template('tag.html',
                           **{'tag': tag,
                              'posts': tag.posts,
                              'category': tag.category})


@blog.route('/about')
def about():
    return render_template('about.html')
