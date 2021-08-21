import os, sys
from sphinx.util.pycompat import execfile_

BASEDIR = os.path.dirname(os.path.abspath(__file__))

orig_root = "flask"
execfile_(os.path.join(BASEDIR, orig_root, 'docs', 'conf.py'), globals())
sys.path.append(BASEDIR)

# intersphinx_mapping for markupsafe is missing in original conf.py
intersphinx_mapping["markupsafe"] = ("https://markupsafe.palletsprojects.com/", None)

# Translation (ja) -----------------------------------------------------
locale_dirs = [os.path.join(BASEDIR, '_locales')]
gettext_compact = False
gettext_uuid = False
#language = 'ja'

# Google Search Console support in ReadTheDocs site --------------------
templates_path = [os.path.join(BASEDIR, '_templates')]

# set google-site-verification from environment variable
html_context['IS_READTHEDOCS'] = os.environ.get("READTHEDOCS", False)
html_context['GOOGLE_SITE_VERIFICATION'] = os.environ.get('GOOGLE_SITE_VERIFICATION', "")


# support for tooltip showing original text ----------------------------
extensions = globals().get("extensions", [])
#extensions.append("sphinxext.showorig")
extensions.append("sphinxext.hoverorig")
extensions.append("readthedocs_ext.readthedocs")

setup_original = setup  # from 'flask/docs/conf.py'

# setup to be called by sphinx -----------------------------------------
def setup(app):
    #import logging
    #logger = logging.getLogger(__name__)
    #logger.info("setup in conf.py is called")

    app.srcdir = os.path.join(BASEDIR, orig_root, 'docs')
    app.confdir = app.srcdir

    setup_original(app)

