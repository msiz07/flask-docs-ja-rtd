# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
SPHINXINTL    = sphinx-intl
LOCALEDIR		  = _locales

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

gettext:
	@$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" $(LOCALEDIR)/pot $(SPHINXOPTS) $(O)

locale: gettext
	@$(SPHINXINTL) update -p $(LOCALEDIR)/pot -d $(LOCALEDIR) -l ja

html_ja: locale
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -D language=ja $(SPHINXOPTS) $(O)

.PHONY: help gettext locale html_ja Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
