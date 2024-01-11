from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="schickit",
    version="0.0.56",
    description="a toolkit for processing single cell Hi-C data",
    author="ABC",
    packages=['schickit', 'schickit.utils'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'schickit = schickit.main:main',
        ]}
)
