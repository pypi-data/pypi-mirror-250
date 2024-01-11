#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dbt-conveyor-snowflake"
# make sure this always matches dbt/adapters/{adapter}/__version__.py
description = """The ConveyorSnowflake adapter plugin for dbt"""

setup(
    name=package_name,
    description=description,
    setuptools_git_versioning={
        "enabled": True,
    },
    long_description=description,
    author="Stijn De Haes",
    author_email="stijn.dehaes@dataminded.be",
    url="https://github.com/datamindedbe/dbt-conveyor-snowflake",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    packages=find_namespace_packages(include=["dbt", "dbt.*"]),
    include_package_data=True,
    install_requires=[
        "dbt-core~=1.7.0",
        "dbt-snowflake~=1.7.0",
    ],
    setup_requires=["setuptools-git-versioning<2"],
)
