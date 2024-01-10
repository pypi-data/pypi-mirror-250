# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['refter', 'refter.tests', 'refter.utils']

package_data = \
{'': ['*'], 'refter.tests': ['fixtures/*']}

install_requires = \
['click',
 'dbt-core>=1.7.4,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.7.0,<14.0.0']

entry_points = \
{'console_scripts': ['refter = refter.cli:cli']}

setup_kwargs = {
    'name': 'refter-cli',
    'version': '0.1.0',
    'description': 'Simple client to validate and push deployments to refter',
    'long_description': '# Overview\n\nSimple client to validate and push deployments to refter\n\n[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/henriblancke/refter-cli/main.yml?branch=main&label=linux)](https://github.com/henriblancke/refter-cli/actions)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/henriblancke/refter-cli.svg?label=windows)](https://ci.appveyor.com/project/henriblancke/refter-cli)\n[![Coverage Status](https://img.shields.io/codecov/c/gh/henriblancke/refter-cli)](https://codecov.io/gh/henriblancke/refter-cli)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/henriblancke/refter-cli.svg)](https://scrutinizer-ci.com/g/henriblancke/refter-cli)\n[![PyPI License](https://img.shields.io/pypi/l/Refter Client.svg)](https://pypi.org/project/Refter Client)\n[![PyPI Version](https://img.shields.io/pypi/v/Refter Client.svg)](https://pypi.org/project/Refter Client)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/Refter Client.svg?color=orange)](https://pypistats.org/packages/Refter Client)\n\n## Setup\n\n### Requirements\n\n* Python 3.10+\n\n### Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install refter-cli\n```\n\n## Usage\n\nCheck out the [refter](https://refter.io/docs) documentation to learn more about how to use the `refter-cli` client.\n',
    'author': 'refter-cli',
    'author_email': 'support@refter.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/refter-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
