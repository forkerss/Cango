from setuptools import find_packages, setup
from Cango import (__author__, __author_email__, __license__, __title__,
                   __url__, __version__)

setup(
    name=__title__,
    version=__version__,
    url=__url__,
    description="A library for executing commands asynchronously.",
    author=__author__,
    author_email=__author_email__,
    keywords='cango',
    license=__license__,
    packages=find_packages(),
    python_requires=">=3.6",
)
