from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'General Purpose/Physics tools'
LONG_DESCRIPTION = 'A library that amalgamates various tools for numerical methods, astroparticle physics simulation analysis, and general-purpose functionalities.'

# Setting up
setup(
    name="chocopearl",
    version=VERSION,
    author="FranciscoLodbrok (Francisco García)",
    author_email="<cfgarcia1903@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    keywords=['python', 'physics', 'general', 'corsika', 'astroparticle', 'numerical methods'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)