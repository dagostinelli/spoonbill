import logging
import click
from . import commands, pack as packcmd
import sys
from datetime import date
import traceback
import json

copyright_string = '%(prog)s %(version)s Copyright ' + str(date.today().year) + ' Darryl T. Agostinelli. All Rights Reserved.'


def main():
	return spoonbill(prog_name="spoonbill")


def process_extra(extra):
	extra_config = dict()
	if extra:
		extras = extra.split(',')
		for item in extras:
			x = item.split('=')

			key = x[0]
			val = x[1]

			# see if val is json
			try:
				val = json.loads(val)
			except:
				# not json
				pass

			extra_config[key] = val

	return extra_config


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


@spoonbill.command()
@click.argument('templates')
@click.argument('config')
@click.argument('page')
@click.argument('extra', nargs=-1)
def compile(templates, config, page, extra):
	"""Compile a single markdown file to html"""
	try:
		print(commands.compile(templates, config, page, process_extra(extra)))
	except Exception as e:
		sys.stderr.write('Error processing page: ' + str(page) + ' : ' + str(e))
		traceback.print_exc()
		exit(1)


@spoonbill.command()
@click.argument('page', type=click.File('rb'))
@click.option('--template-dir', type=click.Path(writable=False))
@click.option('-t', '--template', type=click.Path(writable=False))
@click.option('-c', '--config', type=click.Path(writable=False))
@click.option('-o', '--out', type=click.Path(writable=True))
@click.option('--ignore-errors', is_flag=True, default=False)
@click.option('--inline-config')
def render(page, template_dir, config, out, template, inline_config, ignore_errors):
	"""Render a markdown file to html"""
	inline_config = process_extra(inline_config)
	if template:
		inline_config['template'] = template
	code = commands.compile(page.name, page.read(), template_dir, config, inline_config)
	if out:
		with open(out, 'w') as out_file:
			out_file.write(code)
	click.echo(code)


@spoonbill.command()
@click.argument('config')
@click.argument('path')
@click.argument('extra', nargs=-1)
def structure(config, path, extra):
	"""Alias for sitestructure"""
	print(commands.sitestructure(config, path, process_extra(extra)))


@spoonbill.command()
@click.argument('config')
@click.argument('path')
@click.argument('extra', nargs=-1)
def sitestructure(config, path, extra):
	"""Read all markdown files and make a site structure file"""
	try:
		print(commands.sitestructure(config, path, process_extra(extra)))
	except Exception as e:
		sys.stderr.write('Error processing path: ' + str(path) + ' : ' + str(e))
		traceback.print_exc()
		exit(1)


@spoonbill.command()
@click.argument('input', type=click.File('rb'))
@click.option('-o', '--out', type=click.Path(writable=True))
@click.option('--ignore-errors', is_flag=True, default=False)
def pack(input, out, ignore_errors):
	"""Given an html file, combine all of the images, css and js into a single file"""
	code = packcmd.pack(input.name, input.read(), ignore_errors=ignore_errors)
	if out:
		with open(out, 'w') as out_file:
			out_file.write(code)
	click.echo(code)


if __name__ == "__main__":
	sys.exit(main())
