# support for tooltip showing original text ----------------------------
from os import path
from typing import Any, Dict, List, Tuple, TypeVar
from docutils.utils import relative_path
from docutils.nodes import Node, Element, TextElement
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import init as init_locale
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset
from sphinx.util.i18n import docname_to_domain
from sphinx.util.nodes import extract_messages

logger = logging.getLogger(__name__)

if False:
    # For type annotation
    from typing import Type  # for python3.5.1
    from sphinx.application import Sphinx

class locale_original_text(TextElement): pass
def visit_locale_original_text(self, node):
    self.body.append(self.starttag(node, "span"))
def depart_locale_original_text(self, node):
    self.body.append("</span>")
    #logger.info(node)

original_text_attr = "data-trans-original-text"
original_text_css = "trans-original-text"
translated_text_css= "trans-translated-text"

# custom transform for keep left original text translated, implemented
# based on (mostly copied from) sphinx.transforms.i18n.Locale
class PreserveLocaleOriginalMessage(SphinxTransform):
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

def append_css_class(node, class_) -> None:
    node.coerce_append_attr_list('classes', class_)

class PostProcessTranslatedNode(SphinxTransform):
    """
    Add %s class attribute to translated text node.
    Append locale original text node with %s class to translated text node.
    """ % (translated_text_css, original_text_css)

    #default_priority = 20 # priority of sphinx.transforms.i18n.Locale
    #default_priority = 999 # priority of sphinx.transforms.i18n.RemoveTranslatableInline
    default_priority = 999

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        # XXX check if this is reliable
        settings, source = self.document.settings, self.document['source']
        assert source.startswith(self.env.srcdir)

        for node in self.document.traverse(is_translated_node):
            # add translated_text_css to classes
            append_css_class(node, translated_text_css)

            # append original msg node as literal node
            #orig_text_node = literal(text=node[original_text_attr])
            orig_text_node = locale_original_text(text=node[original_text_attr])
            append_css_class(orig_text_node, original_text_css)
            node.append(orig_text_node)

def setup(app):
    # display builder info to check builder in readthedocs env
    def show_builder_name(event_app):
        logger.info("builder name: %s" % event_app.builder.name)
        logger.info(event_app.builder)
    app.connect('builder-inited', show_builder_name)

    # for original text tooltip support
    def setup_html_builder_extras(event_app):
        lang = event_app.config.language
        if lang is None:
            return
        if not isinstance(event_app.builder, StandaloneHTMLBuilder):
            return
        event_app.add_transform(PreserveLocaleOriginalMessage)
        event_app.add_transform(PostProcessTranslatedNode)
        event_app.add_css_file("trans-tooltip.css")
        visitor_methods = { "html":
                                (visit_locale_original_text,
                                 depart_locale_original_text)
                          }
        event_app.add_node(locale_original_text, **visitor_methods)
    app.connect('builder-inited', setup_html_builder_extras)

    def copy_asset_files(event_app, exception):
        if not exception:
            static_dir = path.join(path.dirname(__file__), "_static")
            out_static_dir = path.join(event_app.outdir, "_static")
            copy_asset(static_dir, out_static_dir, context={})
            #logger.info("static_dir: %s" % static_dir)
            #logger.info("outdir: %s" % out_static_dir)
    app.connect('build-finished', copy_asset_files)

