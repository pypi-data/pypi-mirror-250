# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tempowork']
setup_kwargs = {
    'name': 'tempowork',
    'version': '0.1.3',
    'description': 'A library for mining temporal networks where time is represented as a continuous dimension!',
    'long_description': None,
    'author': 'alijazayeri',
    'author_email': 'jazayeri.ali@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
