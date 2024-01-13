from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.993'
DESCRIPTION = 'usefull tools for data-stories team.'

# Setting up
setup(
    name="mgcomtools",
    version=VERSION,
    author="Mkozyrev (Maksim Kozyrev)",
    author_email="<m.kozyrev@mgcom.ru>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['mgcom'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)