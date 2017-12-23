import os
import re

from setuptools import setup


def rel(*parts):
  '''returns the relative path to a file wrt to the current directory'''
  return os.path.abspath(os.path.join(os.path.dirname(__file__), *parts))

if os.path.isfile('README.rst'):
  README = open('README.rst', 'r').read()
else:
  README = open('README.md', 'r').read()

with open(rel('cljs_loader', '__init__.py')) as handler:
  INIT_PY = handler.read()

VERSION = re.findall("__version__ = '([^']+)'", INIT_PY)[0]

setup(
  name = 'django-cljs-loader',
  long_description = README,
  packages = ['cljs_loader', 'cljs_loader/templatetags'],
  version = VERSION,
  description = 'ClojureScript integration for Django',
  author = 'Johannes Staffans',
  author_email = 'johannes.staffans@gmail.com',
  download_url = 'https://github.com/jstaffans/django-cljs-loader/tarball/{0}'.format(VERSION),
  url = 'https://github.com/jstaffans/django-cljs-loader',
  keywords = ['django', 'clojurescript'],
  install_requires = ['edn-format==0.5.12'],
  classifiers = [
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Framework :: Django',
    'Environment :: Web Environment',
    'License :: OSI Approved :: MIT License',
  ],
)
