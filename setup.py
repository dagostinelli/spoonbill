import sys
from setuptools import setup, find_packages

version = open('VERSION').read().strip()

setup_options = dict(
	name='spoonbill',
	version=version,
	author='Darryl T. Agostinelli',
	author_email='dagostinelli@gmail.com',
	url='http://www.darrylagostinelli.com',
	description='Static website generator',
	long_description=open('README.md').read().strip(),
	package_dir={'': 'src'},  # Our packages live under src but src is not a package itself
	packages=find_packages('src'),
	include_package_data=True,
	install_requires=[
		# put packages here
		'wheel',
		'click',
		'jinja2',
		'BeautifulSoup',
		'markdown',
		'frontmatter'
	],
	test_suite='tests',
	entry_points={
		'console_scripts': [
			'spoonbill=spoonbill.cli:main',
		]
	}
)

if 'py2exe' in sys.argv:
	import py2exe
	setup_options['options'] = {
		'py2exe': {
			'optimize': 0,
			'skip_archive': True,
			'dll_excludes': ['crypt32.dll'],
			'packages': ['urllib', 'httplib']
		}
	}

setup(**setup_options)

