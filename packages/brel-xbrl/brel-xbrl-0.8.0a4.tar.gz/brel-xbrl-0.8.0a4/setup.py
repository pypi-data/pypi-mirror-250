"""Python setup.py for brel package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("brel", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="brel-xbrl",
    version=read("brel", "VERSION"),
    python_requires=">=3.10",
    description="An XBRL parser for Python",
    url="https://github.com/BrelLibrary/brel/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="PapediPoo, ghislainfourny",
    packages=find_packages(exclude=["tests", ".github"]),
    package_data={"brel-xbrl": ["config/*.json"]},
    install_requires=[
        'certifi==2023.11.17',
        'charset-normalizer==3.3.2',
        'idna==3.6',
        'lxml==5.1.0',
        'prettytable==3.9.0',
        'python-dateutil==2.8.2',
        'requests==2.31.0',
        'six==1.16.0',
        'urllib3==2.1.0',
        'wcwidth==0.2.13'
    ],
    entry_points={"console_scripts": ["brel = brel.__main__:main"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    extras_require={"test": read_requirements("requirements-test.txt")},
)
