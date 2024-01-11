from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Access the values of your ProxyOT points and lists.'
LONG_DESCRIPTION = 'A python package that allows you access to your points and lists in ProxyOT. Using this package, you can easily access these values in your Proxyot Apps, as well as your own Python scripts.'

# Setting up
setup(
    name="proxyot",
    version=VERSION,
    author="OchaTEK",
    author_email="<ochatek@ochatek.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'proxyot', 'iot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
