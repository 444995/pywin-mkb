from setuptools import setup, find_packages

setup(
    name='pywin_mkb',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'pywin_mkb=pywin_mkb.main:main',
        ],
    },
)
