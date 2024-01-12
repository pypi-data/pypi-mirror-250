# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectral_datawrappers', 'spectral_datawrappers.credit_scoring']

package_data = \
{'': ['*'], 'spectral_datawrappers': ['config/*']}

install_requires = \
['dynaconf>=3.2.3,<4.0.0',
 'pytest>=7.4.3,<8.0.0',
 'requests>=2.31.0,<3.0.0',
 'tqdm>=4.66.1,<5.0.0']

setup_kwargs = {
    'name': 'spectral-datawrappers',
    'version': '0.2.2',
    'description': "Library for retrieving data for participating in Spectral's challenges",
    'long_description': '# spectral-datawrappers\nCollection of Data Wrappers for Onchain Competitions\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
