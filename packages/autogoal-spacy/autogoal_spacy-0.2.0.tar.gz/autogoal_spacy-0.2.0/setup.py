# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal_spacy']

package_data = \
{'': ['*']}

install_requires = \
['autogoal==1.0.1a0', 'spacy>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'autogoal-spacy',
    'version': '0.2.0',
    'description': 'Spacy algorithm library wrapper for AutoGOAL',
    'long_description': '# AutoGOAL SPACY Algorithm Library',
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
