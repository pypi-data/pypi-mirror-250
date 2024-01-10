# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycountsxch']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3']

setup_kwargs = {
    'name': 'pycountsxch',
    'version': '0.1.3',
    'description': 'Python package to count text',
    'long_description': '# pycounts\n\nCalculate word counts in a text file!\n\n## Installation\n\n```bash\n$ pip install pycountsxch\n```\n\n## Usage\n\n`pycounts` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pycountsxch.pycounts import count_words\nfrom pycountsxch.plotting import plot_words\nimport matplotlib.pyplot as plt\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. \nPlease note that this project is released with a Code of Conduct. \nBy contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycountsxch` was created by Charles Xu. It is licensed under the terms\nof the MIT license.\n\n## Credits\n\n`pycounts` was created with \n[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and \nthe `py-pkgs-cookiecutter` \n[template](https://github.com/py-pkgs/py-pkgs-cookiecutter).',
    'author': 'Charles Xu',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
