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
from docutils.nodes import Node, Element, literal
from sphinx.builders.html import StandaloneHTMLBuilder
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
    Add locale original text to translated nodes as %s attribute.
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

def is_translated_node(node: Node) -> bool:
    if not isinstance(node, Element):
        return False
    return original_text_attr in node.attributes

class AddClassAttributeToLocaleTranslatedNode(SphinxTransform):
    """
    Add %s class attribute to translated text node.
    """ % translated_text_css

    #default_priority = 20 # priority of sphinx.transforms.i18n.Locale
    #default_priority = 999 # priority of sphinx.transforms.i18n.RemoveTranslatableInline
    default_priority = 999

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        # XXX check if this is reliable
        settings, source = self.document.settings, self.document['source']
        assert source.startswith(self.env.srcdir)

        # add translated_text_css to classes
        for node in self.document.traverse(is_translated_node):
              node_classes = node.get("classes", [])
              node_classes.append(translated_text_css)
              node['classes'] = node_classes

class AppendLocaleOriginalMessage(SphinxTransform):
    """
    Append locale original text node with %s class to translated text node.
    """ % translated_text_css

    #default_priority = 20 # priority of sphinx.transforms.i18n.Locale
    #default_priority = 999 # priority of sphinx.transforms.i18n.RemoveTranslatableInline
    default_priority = 999

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        # XXX check if this is reliable
        settings, source = self.document.settings, self.document['source']
        assert source.startswith(self.env.srcdir)

        # append original msg node as literal node
        for node in self.document.traverse(is_translated_node):
            msg = node[original_text_attr]
            orig_text_node = literal(text=msg)
            classes = orig_text_node.attributes.get("classes", [])
            classes.append(original_text_css)
            orig_text_node["classes"] = classes
            node.append(orig_text_node)


# setup to be called by sphinx -----------------------------------------

setup_original = setup  # from 'flask/docs/conf.py'

def setup(app):
    logger = logging.getLogger(__name__)
    #logger.info("setup in conf.py is called")

    app.srcdir = os.path.join(BASEDIR, 'flask', 'docs')
    app.confdir = app.srcdir

    # to check builder in readthedocs env
    def show_builder_name(event_app):
        logger.info("builder name: %s" % event_app.builder.name)
        logger.info(event_app.builder)
    app.connect('builder-inited', show_builder_name)

    # for original text tooltip support
    def add_transform(event_app):
        if isinstance(event_app.builder, StandaloneHTMLBuilder):
            app.add_transform(CopyLocaleOriginalMessageAsAttribute)
            app.add_transform(AddClassAttributeToLocaleTranslatedNode)
            app.add_transform(AppendLocaleOriginalMessage)
    app.connect('builder-inited', add_transform)

    setup_original(app)

    # ``html_static_path`` is initialized in setup_original, so append
    # the current directory's _static subdirectory after setup_original
    html_static_path.append(os.path.join(BASEDIR, '_static'))

