import logging
import click
import jinja2
import json
import os
from bs4 import BeautifulSoup
from markdown import markdown
import frontmatter
import datetime
import time
from datetime import date
import urllib.parse
import traceback


copyright_string = '%(prog)s %(version)s Copyright ' + str(date.today().year) + ' Darryl T. Agostinelli. All Rights Reserved.'


def main():
	return spoonbill(prog_name="spoonbill")


@click.group()
@click.option('--verbose', envvar='SPOONBILL_VERBOSE', is_flag=True, default=False, help='Show detailed step by step logging')
@click.option('--debug', envvar='SPOONBILL_DEBUG', is_flag=True, default=False, help='Show all kinds of low-level messages')
@click.version_option("1.0", prog_name="spoonbill", message=copyright_string)
@click.pass_context
def spoonbill(ctx, verbose, debug, *args, **kwargs):
	"""Spoonbill

	Static website generator
	"""
	# basic logging handler is null
	handlers = [
		logging.NullHandler()
	]

	# basic log level
	loglevel = logging.INFO

	# if debug is on, then output the whole thing to the stream
	if debug:
		handlers.append(logging.StreamHandler())
		loglevel = logging.DEBUG

	logging.basicConfig(
		level=loglevel,
		format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
		datefmt='%H:%M:%S',
		handlers=handlers
	)


def change_file_extension(p, ext):
	basefilename = os.path.splitext(os.path.basename(p))[0]
	filename = basefilename + ext
	filename = os.path.join(os.path.dirname(p), filename)
	return filename


def render_page(templates, template, **data):
	environment = jinja2.Environment(loader=jinja2.FileSystemLoader(templates))
	preprocessed = environment.get_template(template).render(data)
	template = jinja2.Template(preprocessed)
	return template.render(data)


@spoonbill.command()
@click.argument('templates')
@click.argument('config')
@click.argument('page')
@click.argument('extra', nargs=-1)
def compile(templates, config, page, extra):
	"""Compile a single markdown file to html"""
	try:
		extra_config = dict()
		for item in extra:
			x = item.split('=')
			extra_config[x[0]] = x[1]

		with open(config) as defaults_file:
			default_config = json.load(defaults_file)

		raw_markdown = frontmatter.load(page)
		md = raw_markdown.content

		merged = dict()
		merged.update(default_config)
		merged.update(extra_config)
		merged.update(raw_markdown)

		if 'markdown_extensions' in merged:
			markdown_extensions = merged['markdown_extensions']
		else:
			markdown_extensions = []

		merged['content'] = BeautifulSoup(markdown(md, extensions=markdown_extensions), 'html.parser').prettify()

		if 'canonical' not in raw_markdown.keys():
			if 'canonical_relative_path' in merged:
				merged['canonical'] = urllib.parse.urljoin(default_config['canonical'], merged['canonical_relative_path'])
			else:
				merged['canonical'] = urllib.parse.urljoin(default_config['canonical'], change_file_extension(page, '.html'))

		if 'updated' not in merged.keys():
			(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(page)
			merged['updated'] = "%s" % time.ctime(mtime)

		merged['year'] = datetime.datetime.now().year
		merged['templates'] = templates
		merged['page'] = os.path.splitext(os.path.basename(page))[0]
		merged['template'] = change_file_extension(merged['template'], '.html')

		final = render_page(**merged)
		print(final)
	except Exception as e:
		print('Error processing page: ' + str(page) + ' : ' + str(e))
		traceback.print_exc()
		exit(1)
