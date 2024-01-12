# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogoal_gensim']

package_data = \
{'': ['*']}

install_requires = \
['autogoal==1.0.1a0', 'gensim>=4.2,<5.0']

setup_kwargs = {
    'name': 'autogoal-gensim',
    'version': '0.2.0',
    'description': 'Gensim algorithm library wrapper for AutoGOAL',
    'long_description': '# AutoGOAL GENSIM Algorithm Library',
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
