# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['r2io']
install_requires = \
['numpy>=1.26.3,<2.0.0']

setup_kwargs = {
    'name': 'r2io',
    'version': '0.1.1',
    'description': 'Decoding [seismic] r2 files using python.',
    'long_description': None,
    'author': 'Jordan Dennis',
    'author_email': 'jdenn105@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
