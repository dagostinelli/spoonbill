import logging
import click
from . import commands
import sys
from datetime import date
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


@spoonbill.command()
@click.argument('templates')
@click.argument('config')
@click.argument('page')
@click.argument('extra', nargs=-1)
def compile(templates, config, page, extra):
	"""Compile a single markdown file to html"""
	try:
		print(commands.compile(templates, config, page, extra))
	except Exception as e:
		sys.stderr.write('Error processing page: ' + str(page) + ' : ' + str(e))
		traceback.print_exc()
		exit(1)


@spoonbill.command()
@click.argument('config')
@click.argument('path')
@click.argument('extra', nargs=-1)
def structure(config, path, extra):
	"""Alias for sitestructure"""
	print(commands.sitestructure(config, path, extra))


@spoonbill.command()
@click.argument('config')
@click.argument('path')
@click.argument('extra', nargs=-1)
def sitestructure(config, path, extra):
	"""Read all markdown files and make a site structure file"""
	try:
		print(commands.sitestructure(config, path, extra))
	except Exception as e:
		sys.stderr.write('Error processing path: ' + str(path) + ' : ' + str(e))
		traceback.print_exc()
		exit(1)


if __name__ == "__main__":
	sys.exit(main())
