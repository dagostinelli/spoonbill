from setuptools import setup, find_packages

version = open('VERSION').read().strip()

requirements = [
	# put packages here
	'wheel',
	'click',
	'jinja2',
	'beautifulsoup4',
	'markdown',
	'python-frontmatter'
]

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
	install_requires=requirements,
	tests_require=requirements,
	test_suite='tests',
	entry_points={
		'console_scripts': [
			'spoonbill=spoonbill.cli:main',
		]
	}
)

setup(**setup_options)
