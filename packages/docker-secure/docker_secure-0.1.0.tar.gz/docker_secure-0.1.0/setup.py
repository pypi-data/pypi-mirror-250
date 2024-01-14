# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_secure']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.1.4,<3.0.0']

setup_kwargs = {
    'name': 'docker-secure',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Krushna Panchvishe',
    'author_email': 'krushna.4997@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
