# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openpack_toolkit',
 'openpack_toolkit.activity',
 'openpack_toolkit.bin',
 'openpack_toolkit.codalab',
 'openpack_toolkit.codalab.operation_segmentation',
 'openpack_toolkit.configs',
 'openpack_toolkit.configs.datasets',
 'openpack_toolkit.data',
 'openpack_toolkit.utils',
 'openpack_toolkit.validation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'omegaconf>=2.2.2,<3.0.0',
 'pandas>=1.5.2,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['optk-file = openpack_toolkit.bin.file:entry_func']}

setup_kwargs = {
    'name': 'openpack-toolkit',
    'version': '1.1.0',
    'description': 'Toolkit for OpenPack Dataset',
    'long_description': '# OpenPack Dataset Toolkit (optk)\n\n![OpenPack Dataset Logo](./img/OpenPackDataset-black.png)\n\n[![Test](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml)\n[![API Docs - GitHub Pages](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml)\n\n["OpenPack Dataset"](https://open-pack.github.io) is a new large-scale multi modal dataset of manual packing process.\nOpenPack is an open access logistics-dataset for human activity recognition, which contains human movement and package information from 16 distinct subjects.\nThis repository provide utilities to explore our exciting dataset.\n\n## Dataset Release Note\n\n- [OpenPack Dataset (v1.0.0)](https://open-pack.github.io/release/v1-0-0)\n\nFor preliminary analysis, please start from `preprocessed-IMU-with-operation-labels.zip` in [zenodo](https://zenodo.org/records/8145223).\nThis preprocessed dataset include IMU data (acc, gyro, quaternion) assosiated with operatopn labels because you don\'t need to combine data and label.\n\n## Docs\n\n### Dataset\n\n- [Subjects & Recording Scenarios](./docs/USER.md)\n- [Activity Class Definition](./docs/ANNOTATION.md)\n- [Modality](./docs/DATA_STREAM.md)\n- [Data Split (Train/Val/Test/Submission)](./docs/DATA_SPLIT.md)\n\n### Task & Activity Recognition Challenge\n\n- Work Operation Recognition\n  - [OpenPack Challenge 2022](./docs/OPENPACK_CHALLENGE/)\n\n### Sample Data\n\n[Sample](./samples/)\n\n## Install\n\nWe provide some utility functions as python package. You can install via pip with the following command.\nNote that the supported dataset version is `>=1.0.0`.\n\n```bash\n# Pip\npip install openpack-toolkit\n\n# Poetry\npoetry add  openpack-toolkit\n```\n\n## Examples\n\n### Tutorial\n\n- [Download and Visualization (Notebook)](./samples/OpenPack_DataVisualization.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/open-pack/openpack-toolkit/blob/main/samples/OpenPack_DataVisualization.ipynb)\n\n### Work Activity Recognition (PyTorch)\n\nPyTorch code samples for work operation prediction task is available.\nSee [openpack-torch](https://github.com/open-pack/openpack-torch) for more dietail.\n\n### Timestamp\n\nEach data point is associated with a millisecond-precision unix timestamp.\nThe following is a snippet that converts a timestamp (an `int` value) into a `datatime.datetime()` object with timezone.\n\n```python\nimport datetime\n\n\ndef timestamp_to_datetime(ts: int) -> datetime.datetime:\n  """Convert unix timestamp (milli-second precision) into datatime object. """\n  timezone_jst = datetime.timezone(datetime.timedelta(hours=9))\n  dt = datetime.datetime.fromtimestamp(ts / 1000).replace(tzinfo=timezone_jst)\n  return dt\n  \ndef datetime_to_timestamp(dt: datetime.datetime) -> int:\n  """Convert a datetime object into a milli-second precision timestamp."""\n  return int(dt.timestamp() * 1000)\n\n\nts = 1634885786000\n\ndt_out =  timestamp_to_datetime(ts)\nts_out = datetime_to_timestamp(dt_out)\nprint(f"datetime: {dt_out}")  # datetime: 2021-10-22 15:56:26+09:00\nprint(f"timestamp: {ts_out}")  # timestamp: 1634885786000\nassert ts_out == ts\n```\n\n## Download Dataset\n\n### From Zenodo (w/o Depth Images)\n\n```bash\nbash tools/download/dl_from_zenodo.sh <path to a dataset root directory>\n\n# Example:\nbash tools/download/dl_from_zenodo.sh ./data/datasets\n```\n\n## Links\n\n- [Homepage](https://open-pack.github.io/) (External Site)\n  - [OpenPack Challenge 2022](https://open-pack.github.io/challenge2022) (External Site)\n- [zenodo](https://doi.org/10.5281/zenodo.5909086)\n- [API Docs](https://open-pack.github.io/openpack-toolkit/openpack_toolkit/)\n- [PyPI](https://pypi.org/project/openpack-toolkit/)\n- [openpack-torch](https://github.com/open-pack/openpack-torch)\n\n![OpenPack Challenge Logo](./img/OpenPackCHALLENG-black.png)\n\n## License\n\nopenpack-toolkit has a MIT license, as found in the [LICENSE](./LICENCE) file.\n\nNOTE: [OpenPack Dataset](https://doi.org/10.5281/zenodo.5909086) itself is available under [Creative Commons Attribution Non Commercial Share Alike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode) license.\nHowever, [OpenPack Dataset (+RGB) License](./docs/OPENPACK_DATASET_RGB_LICENSE.md) is applied to "OpenPack Dataset (+RGB)" which includs RGB data.\n',
    'author': 'Yoshimura Naoya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://open-pack.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
