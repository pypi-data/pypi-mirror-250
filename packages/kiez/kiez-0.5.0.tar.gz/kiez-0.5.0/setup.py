# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiez',
 'kiez.analysis',
 'kiez.evaluate',
 'kiez.hubness_reduction',
 'kiez.io',
 'kiez.neighbors',
 'kiez.neighbors.approximate',
 'kiez.neighbors.exact']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['class-resolver>=0.3',
 'joblib>=1.2.0,<2.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scikit-learn>=0.24.1,<2.0.0',
 'scipy>=1.3.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'annoy': ['annoy>=1.17.0,<2.0.0'],
 'docs': ['Sphinx>=5.0.0,<6.0.0', 'insegel>=1.3.1,<2.0.0'],
 'ngt': ['ngt>=1.8,<2.0'],
 'nmslib': ['nmslib>=2.1.1,<3.0.0']}

setup_kwargs = {
    'name': 'kiez',
    'version': '0.5.0',
    'description': 'Hubness reduced nearest neighbor search for entity alignment with knowledge graph embeddings',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/kiez/raw/main/docs/kiezlogo.png" alt="kiez logo", width=200/>\n</p>\n\n<h2 align="center"> <a href="https://dbs.uni-leipzig.de/file/KIEZ_KEOD_2021_Obraczka_Rahm.pdf">kiez</a></h2>\n\n<p align="center">\n<a href="https://github.com/dobraczka/kiez/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/kiez/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://kiez.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/kiez/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://pypi.org/project/kiez"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/kiez"></a>\n<a href="https://github.com/dobraczka/kiez/blob/main/LICENSE"><img alt="License BSD3 - Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-blue"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nA Python library for hubness reduced nearest neighbor search for the task of entity alignment with knowledge graph embeddings. The term kiez is a [german word](https://en.wikipedia.org/wiki/Kiez) that refers to a city neighborhood.\n\n## Hubness Reduction\nHubness is a phenomenon that arises in high-dimensional data and describes the fact that a couple of entities are nearest neighbors (NN) of many other entities, while a lot of entities are NN to no one.\nFor entity alignment with knowledge graph embeddings we rely on NN search. Hubness therefore is detrimental to our matching results.\nThis library is intended to make hubness reduction techniques available to data integration projects that rely on (knowledge graph) embeddings in their alignment process. Furthermore kiez incorporates several approximate nearest neighbor (ANN) libraries, to pair the speed advantage of approximate neighbor search with increased accuracy of hubness reduction.\n\n## Installation\nYou can install kiez via pip:\n``` bash\npip install kiez\n```\n\nIf you have a GPU you can make kiez faster by installing [faiss](https://github.com/facebookresearch/faiss) (if you do not already have it in your environment):\n\n``` bash\nconda env create -n kiez-faiss python=3.10\nconda activate kiez-faiss\nconda install -c pytorch -c nvidia faiss-gpu=1.7.4 mkl=2021 blas=1.0=mkl\npip install kiez\n```\n\nFor more information see their [installation instructions](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md).\n\nYou can also get other specific libraries with e.g.:\n\n``` bash\n  pip install kiez[nmslib]\n```\n\n## Usage\nSimple nearest neighbor search for source entities in target space:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# fit and get neighbors\nk_inst = Kiez()\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\nUsing (A)NN libraries and hubness reduction methods:\n``` python\nfrom kiez import Kiez\nimport numpy as np\n# create example data\nrng = np.random.RandomState(0)\nsource = rng.rand(100,50)\ntarget = rng.rand(100,50)\n# prepare algorithm and hubness reduction\nalgo_kwargs = {"n_candidates": 10}\nk_inst = Kiez(n_neighbors=5, algorithm="Faiss" algorithm_kwargs=algo_kwargs, hubness="CSLS")\n# fit and get neighbors\nk_inst.fit(source, target)\nnn_dist, nn_ind = k_inst.kneighbors()\n```\n\n## Torch Support\nBeginning with version 0.5.0 torch can be used, when using `Faiss` as NN library:\n\n```python\n\n    from kiez import Kiez\n    import torch\n    source = torch.randn((100,10))\n    target = torch.randn((200,10))\n    k_inst = Kiez(algorithm="Faiss", hubness="CSLS")\n    k_inst.fit(source, target)\n    nn_dist, nn_ind = k_inst.kneighbors()\n```\n\nYou can also utilize tensor on the GPU:\n\n```python\n\n    k_inst = Kiez(algorithm="Faiss", algorithm_kwargs={"use_gpu":True}, hubness="CSLS")\n    k_inst.fit(source.cuda(), target.cuda())\n    nn_dist, nn_ind = k_inst.kneighbors()\n```\n\n## Documentation\nYou can find more documentation on [readthedocs](https://kiez.readthedocs.io)\n\n## Benchmark\nThe results and configurations of our experiments can be found in a seperate [benchmarking repository](https://github.com/dobraczka/kiez-benchmarking)\n\n## Citation\nIf you find this work useful you can use the following citation:\n```\n@article{obraczka2022fast,\n  title={Fast Hubness-Reduced Nearest Neighbor Search for Entity Alignment in Knowledge Graphs},\n  author={Obraczka, Daniel and Rahm, Erhard},\n  journal={SN Computer Science},\n  volume={3},\n  number={6},\n  pages={1--19},\n  year={2022},\n  publisher={Springer},\n  url={https://link.springer.com/article/10.1007/s42979-022-01417-1},\n  doi={10.1007/s42979-022-01417-1},\n}\n```\n\n## Contributing\nPRs and enhancement ideas are always welcome. If you want to build kiez locally use:\n```bash\ngit clone git@github.com:dobraczka/kiez.git\ncd kiez\npoetry install\n```\nTo run the tests (given you are in the kiez folder):\n```bash\npoetry run pytest tests\n```\n\nOr install [nox](https://github.com/theacodes/nox) and run:\n```\nnox\n```\nwhich checks all the linting as well.\n\n## License\n`kiez` is licensed under the terms of the BSD-3-Clause [license](LICENSE.txt).\nSeveral files were modified from [`scikit-hubness`](https://github.com/VarIr/scikit-hubness),\ndistributed under the same [license](external/SCIKIT_HUBNESS_LICENSE.txt).\nThe respective files contain the following tag instead of the full license text.\n\n        SPDX-License-Identifier: BSD-3-Clause\n\nThis enables machine processing of license information based on the SPDX\nLicense Identifiers that are here available: https://spdx.org/licenses/\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dobraczka/kiez',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
