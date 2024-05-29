from setuptools import setup, find_packages

setup(
    name='pywin_mouse',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'pywin_mouse=pywin_mouse.main:main',
        ],
    },
)
