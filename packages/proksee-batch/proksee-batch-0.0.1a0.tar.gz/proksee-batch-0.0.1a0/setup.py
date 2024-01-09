# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['proksee-batch']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['proksee-batch = proksee-batch.__main__:main']}

setup_kwargs = {
    'name': 'proksee-batch',
    'version': '0.0.1a0',
    'description': 'Proksee Batch',
    'long_description': "# Proksee Batch\n\n[![PyPI](https://img.shields.io/pypi/v/proksee-batch.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/proksee-batch.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/proksee-batch)][python version]\n[![License](https://img.shields.io/pypi/l/proksee-batch)][license]\n\n[![Read the documentation at https://proksee-batch.readthedocs.io/](https://img.shields.io/readthedocs/proksee-batch/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/laelbarlow/proksee-batch/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/laelbarlow/proksee-batch/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/proksee-batch/\n[status]: https://pypi.org/project/proksee-batch/\n[python version]: https://pypi.org/project/proksee-batch\n[read the docs]: https://proksee-batch.readthedocs.io/\n[tests]: https://github.com/laelbarlow/proksee-batch/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/laelbarlow/proksee-batch\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Proksee Batch_ via [pip] from [PyPI]:\n\n```console\n$ pip install proksee-batch\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Proksee Batch_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/laelbarlow/proksee-batch/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/laelbarlow/proksee-batch/blob/main/LICENSE\n[contributor guide]: https://github.com/laelbarlow/proksee-batch/blob/main/CONTRIBUTING.md\n[command-line reference]: https://proksee-batch.readthedocs.io/en/latest/usage.html\n",
    'author': 'Lael D. Barlow',
    'author_email': 'lael@ualberta.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laelbarlow/proksee-batch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
