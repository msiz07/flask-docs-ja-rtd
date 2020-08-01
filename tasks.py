from invoke import task, run

import os
from pprint import pprint

# You can edit these variables
SETTINGS = dict(
  SPHINXOPTS = "",
  SPHINXBUILD = "sphinx-build",
  SOURCEDIR = ".",
  BUILDDIR = "_build",
  SPHINXINTL = "sphinx-intl",
  LOCALE = "ja",
  LOCALEDIR = "_locales"
)

@task(help={"target": "target used by sphinx-build"})
def build(ctx, target):
  """Run sphinx-build with provided target"""
  SETTINGS['target'] = target
  print("### SETTING ###")
  pprint(SETTINGS)
  run("{SPHINXBUILD} -M {target} {SOURCEDIR} {BUILDDIR} {SPHINXOPTS}" \
          .format(**SETTINGS))

@task
def list_target(ctx):
  """List targets available by sphinx-build"""
  build(ctx, "help")

@task
def clean(ctx):
  """Remove everything under BUILD ({BUILD}) directory"""
  build(ctx, "clean")

@task
def gettext(ctx):
  """Generate pot files (run: sphinx-build -b gettext)"""
  run("{SPHINXBUILD} -b gettext {SOURCEDIR} {LOCALEDIR}/pot {SPHINXOPTS}" \
          .format(**SETTINGS))

@task
def locale(ctx):
  """Generate locale mo,po files (run: sphinx-intl update)"""
  run("{SPHINXINTL} update -p {LOCALEDIR}/pot -l {LOCALE} {SPHINXOPTS}" \
          .format(**SETTINGS))

@task
def trans_stat(ctx):
  """Output translation stat (run: sphinx-intl stat)"""
  run("{SPHINXINTL} stat -d {LOCALEDIR} -l {LOCALE} {SPHINXOPTS}" \
          .format(**SETTINGS))

@task
def html_trans(ctx):
  """Generate ja translated html files"""
  SETTINGS['SPHINXOPTS'] += " -D language={LOCALE} ".format(**SETTINGS)
  build(ctx,target="html")


@task
def rtd_trans(ctx):
  """Generate ja translated html files with rtd extensions"""
  SETTINGS['SPHINXOPTS'] += " -D language={LOCALE} ".format(**SETTINGS)
  build(ctx,target="readthedocs")


# task(s) for git / work environment
@task
def update_git_submodule(ctx):
  """Update git submodule then sync with its requirements.txt"""
  run("git submodule update")
  flask_docs_req = open(os.path.join("flask","docs","requirements.txt"))
  with open("requirements.txt", "w") as f_out:
    f_out.write(flask_docs_req.read())
    f_out.write("# install current flask under 'flask' submodule\n")
    f_out.write("./flask\n")

@task(update_git_submodule)
def update_tools(ctx):
  """Update tools with requirements.txt content"""
  run("pip install -U -e . -r requirements.txt --progress-bar=off")
