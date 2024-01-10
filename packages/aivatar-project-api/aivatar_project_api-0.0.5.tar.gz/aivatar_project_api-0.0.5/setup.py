"""Describe our module distribution to Distutils."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import third-party modules
from setuptools import find_packages
from setuptools import setup

setup(
    name="aivatar_project_api",
    author="lavenderyao",
    author_email="lavenderyao@tencent.com",
    url="https://git.woa.com/DCC_Client/Framework/aivatar_project_api.git",
    package_dir={"": "."},
    packages=find_packages("."),
    description="API to operate project-info of users in Aivatar products, e.g. get list, choose project...",
    entry_points={},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=['requests>=2.25.1'],
    package_data={
        "": ["*.json"],
    }
)
