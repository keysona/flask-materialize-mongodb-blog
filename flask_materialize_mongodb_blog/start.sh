#!/bin/bash

export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon flask-blog

nohup \
gunicorn -w 4 -b 127.0.0.1:5001 \
--error-logfile /var/log/error-flask-blog.log \
--access-logfile /var/log/access-flask-blog.log \
manage:app 1>/dev/null 2>&1 \
&
