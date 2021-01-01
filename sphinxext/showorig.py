# support for tooltip showing original text ----------------------------
from typing import Any, Text
from os import path
from docutils.utils import relative_path
from docutils.nodes import Node, Element, TextElement
from docutils.writers._html_base import HTMLTranslator
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import init as init_locale
from sphinx.transforms import SphinxTransform
from sphinx.util import logging
from sphinx.util.fileutil import copy_asset
from sphinx.util.i18n import docname_to_domain
from sphinx.util.nodes import extract_messages

logger = logging.getLogger(__name__)


class LocaleOriginalText(TextElement):
    pass


def visit_locale_original_text(self: HTMLTranslator, node: TextElement) -> None:
    self.body.append(self.starttag(node, "span"))


def depart_locale_original_text(self: HTMLTranslator, node: TextElement) -> None:
    self.body.append("</span>")
    # logger.info(node)


ORIGINAL_TEXT_ATTR = "data-trans-original-text"
ORIGINAL_TEXT_CSS = "trans-original-text"
TRANSLATED_TEXT_CSS = "trans-translated-text"


# custom transform for keep left original text translated, implemented
# based on (mostly copied from) sphinx.transforms.i18n.Locale
class PreserveLocaleOriginalMessage(SphinxTransform):
    """
    Add locale original text to translated nodes as %s attribute.
    """ % ORIGINAL_TEXT_ATTR

    # 20 is the priority of sphinx.transforms.i18n.Locale
    default_priority = 15
    # default_priority = 20

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        source = self.document["source"]
        msgstr = ""

        # XXX check if this is reliable
        assert source.startswith(self.env.srcdir)
        docname = path.splitext(
            relative_path(path.join(self.env.srcdir, "dummy"), source)
        )[0]
        textdomain = docname_to_domain(docname, self.config.gettext_compact)

        # fetch translations
        dirs = [
            path.join(self.env.srcdir, directory)
            for directory in self.config.locale_dirs
        ]
        catalog, has_catalog = init_locale(dirs, self.config.language, textdomain)
        if not has_catalog:
            return

        # preserve original msg of translated one as ORIGINAL_TEXT_ATTR attribute
        for node, msg in extract_messages(self.document):
            msgstr = catalog.gettext(msg)
            if not msgstr or msgstr == msg or not msgstr.strip():
                # as-of-yet untranslated
                continue
            # self.logger.info("add %s attr to node." % ORIGINAL_TEXT_ATTR)
            node[ORIGINAL_TEXT_ATTR] = msg


def is_translated_node(node: Node) -> bool:
    if not isinstance(node, Element):
        return False
    return ORIGINAL_TEXT_ATTR in node.attributes


def append_css_class(node: Element, class_: Text) -> None:
    node.coerce_append_attr_list("classes", class_)


class PostProcessTranslatedNode(SphinxTransform):
    """
    Add %s class attribute to translated text node.
    Append locale original text node with %s class to translated text node.
    """ % (
        TRANSLATED_TEXT_CSS,
        ORIGINAL_TEXT_CSS,
    )

    # 20 is the priority of sphinx.transforms.i18n.Locale
    # 80 is the priority of sphinx.transforms.i18n.RemoveTranslatableInline
    default_priority = 999
    # default_priority = 20
    # default_priority = 999

    logger = logging.getLogger(__name__)

    def apply(self, **kwargs: Any) -> None:
        # XXX check if this is reliable
        source = self.document["source"]
        assert source.startswith(self.env.srcdir)

        for node in self.document.traverse(is_translated_node):
            # add TRANSLATED_TEXT_CSS to classes
            append_css_class(node, TRANSLATED_TEXT_CSS)

            # append original msg node as literal node
            # orig_text_node = literal(text=node[ORIGINAL_TEXT_ATTR])
            orig_text_node = LocaleOriginalText(text=node[ORIGINAL_TEXT_ATTR])
            append_css_class(orig_text_node, ORIGINAL_TEXT_CSS)
            node.append(orig_text_node)


def setup(app: Sphinx) -> None:
    # display builder info to check what builder is used
    # e.g. to check the builder in external env such as readthedocs
    def show_builder_name(event_app: Sphinx) -> None:
        logger.info("builder name: %s" % event_app.builder.name)
        logger.info(event_app.builder)

    app.connect("builder-inited", show_builder_name)

    # for original text tooltip support
    def setup_html_builder_extras(event_app: Sphinx) -> None:
        lang = event_app.config.language  # type: ignore
        if lang is None:
            return
        if not isinstance(event_app.builder, StandaloneHTMLBuilder):
            return
        event_app.add_transform(PreserveLocaleOriginalMessage)
        event_app.add_transform(PostProcessTranslatedNode)
        event_app.add_css_file("trans-tooltip.css")
        # register new Node type with vistor methods
        event_app.add_node(
            LocaleOriginalText,
            html=(visit_locale_original_text, depart_locale_original_text),
        )

    app.connect("builder-inited", setup_html_builder_extras)

    def copy_asset_files(event_app: Sphinx, exception: Exception) -> None:
        if not exception:
            static_dir = path.join(path.dirname(__file__), "_static")
            out_static_dir = path.join(event_app.outdir, "_static")
            copy_asset(static_dir, out_static_dir, context={})
            # logger.info("static_dir: %s" % static_dir)
            # logger.info("outdir: %s" % out_static_dir)

    app.connect("build-finished", copy_asset_files)
