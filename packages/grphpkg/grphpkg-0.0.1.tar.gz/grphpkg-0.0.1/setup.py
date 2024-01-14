from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Graph package'

# Setting up
setup(
    name="grphpkg",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="vudiep411@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "matplotlib"
    ],
    keywords=['python', 'data structure', 'graph'],
)