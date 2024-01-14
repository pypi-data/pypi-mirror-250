from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Graph package'
LONG_DESCRIPTION = """
Calculation with very large number
"""

# Setting up
setup(
    name="infp",
    version=VERSION,
    author="Vu Diep",
    author_email="vudiep411@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'data structure', 'math', 'big number', 'infinite precision'],
)