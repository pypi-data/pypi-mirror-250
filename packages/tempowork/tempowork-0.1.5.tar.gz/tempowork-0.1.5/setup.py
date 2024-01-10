# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tempowork']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tempowork',
    'version': '0.1.5',
    'description': 'A library for mining temporal networks where time is represented as a continuous dimension!',
    'long_description': None,
    'author': 'alijazayeri',
    'author_email': 'jazayeri.ali@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
