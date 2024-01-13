import os
from setuptools import (
    find_packages,
    setup,
)
from pathlib import Path

import csb43

# Utility function to read the README file.
# Used for the long_description.


def read(fname):
    path = Path(os.path.dirname(__file__))
    try:
        with open(path / fname, 'r', encoding='utf-8') as fd:
            return fd.read()
    except Exception:
        return ''


try:
    from babel.messages import frontend as babel  # noqa: F401

    entry_points = """
    [distutils.commands]
    compile_catalog = babel:compile_catalog
    extract_messages = babel:extract_messages
    init_catalog = babel:init_catalog
    update_catalog = babel:update_catalog
    """
except ImportError:
    pass

requirements = [
    "pycountry>=16.10.23rc1",
    "importlib_resources;python_version<'3.9'",
    ]

req_tablib = "tablib%s>=0.11.3,<=4.0.0"


setup(
    name="csb43",
    version=csb43.__version__,
    author="wmj",
    author_email="wmj.py@gmx.com",
    description=csb43.__doc__,
    license="LGPL",
    python_requires='>=3.6',
    keywords=(
        "csb csb43 aeb aeb43 homebank ofx Spanish bank ods tsv "
        "xls xlsx excel yaml json html"
    ),
    url="https://bitbucket.org/wmj/csb43",
    project_urls={
        'Bug Reports': 'https://bitbucket.org/wmj/csb43/issues',
        'Source': 'https://bitbucket.org/wmj/csb43',
    },
    packages=find_packages(),
    long_description=(
        read('README.rst') + read('INSTALL') + read('CHANGELOG')
    ),
    scripts=["csb2format"],
    #'requires': requirements,
    install_requires=requirements,
    tests_require=requirements + ["lxml"],
    include_package_data=True,
    extras_require={
        'babel': ["Babel"],
        'yaml': ['PyYAML'],
        'basic_formats': [req_tablib % ""],
        'formats': [req_tablib % "[all]"],
        'all': ["PyYAML", req_tablib % "[all]"],
    },
    test_suite='csb43.tests',
    #'package_data': {
    #    'i18n': ['csb43/i18n/*']
    #},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: GNU Lesser General "
        "Public License v3 (LGPLv3)"
    ]
)
