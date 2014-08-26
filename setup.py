# coding=utf-8
from setuptools import setup
from os import path

from pynoramio import __version__

base_dir = path.abspath(path.dirname(__file__))

setup(
    name='Pynoramio',
    version=__version__,
    description='Python SDK for the Panoramio data API (http://panoramio.com/api/data/api.html)',
    url='https://github.com/boisei0/pynoramio',
    author='Rob Derksen',
    author_email='rob.derksen@hubsec.eu',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='api maps panoramio',
    install_requires=['requests'],
    packages=['pynoramio']
)