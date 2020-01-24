import os
from sphinx.util.pycompat import execfile_

BASEDIR = os.path.dirname(os.path.abspath(__file__))

execfile_(os.path.join(BASEDIR, 'flask', 'docs', 'conf.py'), globals())


# Translation (ja) -----------------------------------------------------
locale_dirs = [os.path.join(BASEDIR, '_locales')]
gettext_compact = False
gettext_uuid = True
#language = 'ja'

# Google Search Console support in ReadTheDocs site --------------------
templates_path = [os.path.join(BASEDIR, '_templates')]

# set google-site-verification from environment variable
import os
html_context['IS_READTHEDOCS'] = os.environ.get("READTHEDOCS", False)
html_context['GOOGLE_SITE_VERIFICATION'] = os.environ.get('GOOGLE_SITE_VERIFICATION', "DUMMY")

# support for tooltip showing original text ----------------------------
from os import path
from typing import Any, Dict, List, Tuple, TypeVar
from docutils.utils import relative_path
from sphinx.locale import init as init_locale
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.i18n import docname_to_domain
from sphinx.util.nodes import extract_messages

if False:
    # For type annotation
    from typing import Type  # for python3.5.1
    from sphinx.application import Sphinx

original_text_attr = "data-trans-original-text"
original_text_css = "trans-original-text"
translated_text_css= "trans-translated-text"

# custom transform for keep left original text translated, implemented
# based on (mostly copied from) sphinx.transforms.i18n.Locale
class CopyLocaleOriginalMessageAsAttribute(SphinxTransform):
    """
    Add original text to translated nodes as %s attribute.
    """ % original_text_attr

    #default_priority = 20 # priority of sphinx.transforms.i18n.Locale
    default_priority = 15

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        settings, source = self.document.settings, self.document['source']
        msgstr = ''

        # XXX check if this is reliable
        assert source.startswith(self.env.srcdir)
        docname = path.splitext(relative_path(path.join(self.env.srcdir, 'dummy'),
                                              source))[0]
        textdomain = docname_to_domain(docname, self.config.gettext_compact)

        # fetch translations
        dirs = [path.join(self.env.srcdir, directory)
                for directory in self.config.locale_dirs]
        catalog, has_catalog = init_locale(dirs, self.config.language, textdomain)
        if not has_catalog:
            return

        # preserve original msg of translated one as original_text_attr attribute
        for node, msg in extract_messages(self.document):
            msgstr = catalog.gettext(msg)
            if not msgstr or msgstr == msg or not msgstr.strip():
                # as-of-yet untranslated
                continue
            #self.logger.info("add %s attr to node." % original_text_attr)
            node[original_text_attr] = msg

from sphinx.util.docutils import is_html5_writer_available
if not is_html5_writer_available():
    from sphinx.writers.html import HTMLTranslator
else:
    from sphinx.writers.html5 import HTML5Translator as HTMLTranslator

class KeepLocaleOriginalMessageHTMLTranslator(HTMLTranslator):
    from sphinx.util import logging
    logger = logging.getLogger(__name__)

    def dispatch_visit(self, node):
        """
        Add "%s" to class attribute if node has "%s" attr.

        After the above, call "super().``dispatch_visit`` + node class name"
        with `node` as parameter.
        """ % (translated_text_css, original_text_attr)

        if node.__dict__.get("attributes", False):
            if node.__dict__.get("attributes").get(original_text_attr, False):
              node_classes = node.get("classes", [])
              node_classes.append(translated_text_css)
              node['classes'] = node_classes

        return super().dispatch_visit(node)

    def dispatch_departure(self, node):
        """
        Add ``<span>`` with "%s" css class for translation original text just
        before close tag if node has "%s" attr.

        After the above, call super()."``dispatch_departure`` + node class name"
        with `node` as parameter.
        """ % (original_text_css, original_text_attr)

        if node.__dict__.get('attributes', False):
            if node.__dict__.get('attributes').get(original_text_attr, False):
                self.body.append("""<span class="%s">""" % original_text_css)
                self.body.append("%s" % node.get(original_text_attr))
                self.body.append("</span>" )

        return super().dispatch_departure(node)


# setup to be called by sphinx -----------------------------------------

setup_original = setup  # from 'flask/docs/conf.py'

def setup(app):
    from sphinx.util import logging
    #logger = logging.getLogger(__name__)
    #logger.info("setup in conf.py is called")

    app.srcdir = os.path.join(BASEDIR, 'flask', 'docs')
    app.confdir = app.srcdir

    # for original text tooltip support
    app.add_transform(CopyLocaleOriginalMessageAsAttribute)
    app.registry.add_translator("html", KeepLocaleOriginalMessageHTMLTranslator)

    setup_original(app)

    # ``html_static_path`` is initialized in setup_original, so append
    # the current directory's _static subdirectory after setup_original
    html_static_path.append(os.path.join(BASEDIR, '_static'))

