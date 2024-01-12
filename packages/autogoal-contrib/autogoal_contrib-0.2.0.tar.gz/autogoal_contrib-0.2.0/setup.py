# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal_contrib', 'autogoal_contrib.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.6,<2.0.0']

setup_kwargs = {
    'name': 'autogoal-contrib',
    'version': '0.2.0',
    'description': 'Common library for AutoGOAL contrib packages',
    'long_description': '# AutoGOAL Contrib Common',
    'author': 'Suilan Estevez-Velarde',
    'author_email': 'suilanestevez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://autogoal.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.16',
}


setup(**setup_kwargs)
