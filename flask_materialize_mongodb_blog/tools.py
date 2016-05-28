import logging

from flask import flash
from flask.ext.admin.babel import gettext
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.admin.contrib.mongoengine.helpers import format_error
from markdown2 import Markdown as Md

log = logging.getLogger("flask-admin.mongo")


class Markdown(Md):

    def __init__(self, html4tags=False, tab_width=4, safe_mode=None,
                 extras=None, link_patterns=None, use_file_vars=False):
        super().__init__(html4tags=html4tags, tab_width=tab_width, safe_mode=safe_mode,
                         extras=extras, link_patterns=link_patterns, use_file_vars=use_file_vars)

    def preprocess(self, text):
        return text

    def postprocess(self, text):
        return text


def markdown(text, html4tags=False, tab_width=4, safe_mode=None,
             extras=None, link_patterns=None, use_file_vars=False):
    return Markdown(html4tags=html4tags, tab_width=tab_width, safe_mode=safe_mode,
                    extras=extras, link_patterns=link_patterns, use_file_vars=use_file_vars).convert(text)


def format_datetime(datetime):
    return "%s年%s月%s日 %s:%s" % (datetime.year, datetime.month, datetime.day,
                                  datetime.hour, datetime.second)


def my_truncate(s, max_line=30):
    lines = s.split('\n')
    count = 0
    has_code = False
    start_code_line = 0
    for line in lines:
        if '<code>' in line:
            has_code = True
            start_code_line = count
        elif '</code>' in line:
            has_code = False
        elif count == max_line:
            break
        count = count + 1
    if has_code:
        return '\n'.join(lines[:start_code_line])
    return '\n'.join(lines[:max_line])


if __name__ == '__main__':
    content = """
I did these things:
* bullet1
* bullet2
* bullet3
"""
#     content = """
# ```
# <script type="text/javascript" src="{{ static_url('shadowbox/shadowbox.js') }}">
# </script>
# <script type="text/javascript">
# Shadowbox.init({ handleOversize: "drag" });
# window.onload = function() {
#     Shadowbox.setup(".entry-content img", { gallery: "{{post.title}}", counterType: "skip" });
# };
# </script>
# ```
# """
#     content = """
# This is python code.
# ```
# print 'hello'
# ```
# """
#     content = """
# ```python
# #!/usr/bin/env python
# ```
# """
    result = markdown(content, extras=['metadata', 'cuddled-lists'])
    print(result)
    print(result.metadata)
