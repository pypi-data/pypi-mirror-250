# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autort']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'zetascale']

setup_kwargs = {
    'name': 'autort-swarms',
    'version': '0.0.1',
    'description': 'AutoRT - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# AutoRT\nImplementation of AutoRT: "AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents". This repo will implement the multi agent system that transforms a scene into a list of ranked and priortized tasks for an robotic action model to execute. This is an very effective setup that I personally beleive is the future for swarming robotic foundation models!\n\nThis project will be implemented using Swarms, for the various llms and use the official RT-1 as the robotic action model.\n\n## Install\n\n\n\n\n## Citation\n```bibtext\n@inproceedings{\n    anonymous2023autort,\n    title={Auto{RT}: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents},\n    author={Anonymous},\n    booktitle={Submitted to The Twelfth International Conference on Learning Representations},\n    year={2023},\n    url={https://openreview.net/forum?id=xVlcbh0poD},\n    note={under review}\n}\n\n```\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AutoRT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
