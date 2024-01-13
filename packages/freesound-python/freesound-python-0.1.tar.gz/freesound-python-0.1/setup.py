from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
    
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
    
VERSION = '0.0.1'
DESCRIPTION = 'Dependency confusion P0C',
#LONG_DESCRIPTION = 'Python package dependency confiuse vulnerability POC.'
    
# Setting up
setup(
    name="freesound-python",
    version="0.1",
    author="nvk0x",
    author_email="naveenkumawat1995@gmail.com",
    description="dependency confusion",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'discord'],
    keywords=[]
   )


