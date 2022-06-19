import pathlib

from pip._internal.req import parse_requirements
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='DBSyncTool',
    version='1.0.0',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=['dbsync'],
    include_package_data=True,
    install_reqs=parse_requirements('requirements.txt', session='hack'),
    entry_points={
        "console_scripts": [
            "dbsync=dbsync.main:main",
        ]
    },
    url='https://github.com/ManishVisave/DBSync',
    license='',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    author='manish visave',
    author_email='manishvisave149@gmail.com',
    description='Syncs PROD metadata with local for assistance in script conversion',
)
