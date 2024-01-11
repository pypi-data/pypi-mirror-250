from setuptools import setup, find_packages

setup(
    name='FreeFireGETinfo',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'FreeFireGETinfo = FreeFireGETinfo.main:main',
        ],
    },
)
