#!/usr/bin/env python2

from distutils.core import setup
import os

# The directory containing this file
HERE = os.path.dirname(__file__)

def readme():
	with open('README.md') as f:
		return f.read()

exec(open('simaconv/_version.py').read())

setup(name='tsharvest',
		version=__version__,
		description='Tool to convert SIMA csv files to shapefile format',
		long_description=readme(),
		long_description_content_type='text/markdown',
		url="https://github.com/fdfoneill/simaconv",
		author="F. Dan O'Neill",
		author_email='fdfoneill@gmail.com',
		license='MIT',
		packages=['simaconv'],
		include_package_data=True,
		# third-party dependencies
		install_requires=[
			'arcpy'
			],
		# classifiers
		classifiers=[
			"License :: OSI Approved :: MIT License",
			"Programming Language :: Python :: 2",
			],

		zip_safe=False,
		# console scripts
		entry_points = {
			'console_scripts': [
				'simaparse=simaconv.simafile:main'
				],
			}
		)
