#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='r2papi',
	version='0.1.0',
	packages=['r2papi'],
	description='High level API on top of r2pipe',
	long_description_content_type='text/markdown',
	long_description=long_description,
	url='https://rada.re',
	author='radare2',
	install_requires=['r2pipe'],
	project_urls={
		'Source': 'https://github.com/radare/radare2-r2papi/',
	},
)
