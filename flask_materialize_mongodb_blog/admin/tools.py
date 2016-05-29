from markdown2 import Markdown as Md


class Markdown(Md):

    def __init__(self, html4tags=False, tab_width=4, safe_mode=None,
                 extras=None, link_patterns=None, use_file_vars=False):

        super().__init__(html4tags=html4tags, tab_width=tab_width,
                         safe_mode=safe_mode, extras=extras,
                         link_patterns=link_patterns,
                         use_file_vars=use_file_vars)

    def preprocess(self, text):
        return text

    def postprocess(self, text):
        return text


def markdown(text, html4tags=False, tab_width=4, safe_mode=None,
             extras=None, link_patterns=None, use_file_vars=False):

    return Markdown(html4tags=html4tags, tab_width=tab_width,
                    safe_mode=safe_mode, extras=extras,
                    link_patterns=link_patterns,
                    use_file_vars=use_file_vars).convert(text)


def format_datetime(view, context, model, name):
    datetime = model[name]
    return "%s年%s月%s日 %s:%s" % (datetime.year, datetime.month, datetime.day,
                                datetime.hour, datetime.second)
