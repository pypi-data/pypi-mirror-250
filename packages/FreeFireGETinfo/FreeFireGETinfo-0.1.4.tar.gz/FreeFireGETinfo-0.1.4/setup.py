# setup.py
from setuptools import setup, find_packages

setup(
    name='FreeFireGETinfo',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
    ],
    entry_points={
        'console_scripts': [
            'FreeFireGETinfo = FreeFireGETinfo.main:main',
        ],
    },
    package_data={
        'FreeFireGETinfo': ['config.ini'],
    },
)
