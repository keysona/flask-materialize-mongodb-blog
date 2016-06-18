#!/bin/bash
echo $VIRTUALENVWRAPPER_HOOK_DIR
VIRTUALENV_DIR=$VIRTUALENVWRAPPER_HOOK_DIR
FLASK_BLOG_ENV=flask-blog
echo $VIRTUALENV_DIR/$FLASK_BLOG_ENV/bin/activate
source $VIRTUALENV_DIR/$FLASK_BLOG_ENV/bin/activate
nohup gunicorn -w 4 --access-logfile /var/log/access-flask-blog.log --error-logfile /var/log/error-flask-blog.log -b 127.0.0.1:8080 manage:app 1>/dev/null 2>&1 &
