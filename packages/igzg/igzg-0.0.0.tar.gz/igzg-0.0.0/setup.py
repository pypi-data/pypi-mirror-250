from setuptools import setup, find_packages
from igzg import __version__ as igzgVersion

setup(
    name = 'igzg',
    version = igzgVersion,
    description = 'PYPI tutorial package creation written by suhyeojee',
    author = 'suhyeojee',
    author_email = 'suhyeojee@gmail.com',
    url = 'https://github.com/suhyeojee/igzg',
    packages = find_packages(exclude=[]),
    package_data = {},
    include_package_data = False,
    zip_safe = False,
    classifiers = [
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires = '>=3.6',
    install_requires = [],
)

