# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause

from setuptools import setup
import intlab

DESCRIPTION = "IISL: SAP-net"
NAME = 'intlab'
AUTHOR = 'Sora Takaya'
AUTHOR_EMAIL = 'so12ra16@outlook.jp'
URL = 'https://github.com/takayasora/intlab'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/takayasora/intlab'
VERSION = intlab.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    "pillow>=9.5.0",
    "matplotlib>=3.7.1",
    "pandas>=2.0.0",
    "numpy>=1.23.5",
    "seaborn>=0.12.2",
    "japanize-matplotlib>=1.1.3",
    "networkx>=3.1"
]

PACKAGES = [
    'intlab'
]

CLASSIFIERS = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
]

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
#long_description = readme 

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",  # もしくは適切なコンテンツタイプを指定
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )
