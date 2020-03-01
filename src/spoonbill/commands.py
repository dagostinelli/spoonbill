import jinja2
import json
import os
from bs4 import BeautifulSoup
from markdown import markdown
import frontmatter
import time
import urllib.parse
import glob
from dateutil.parser import parse as parsedatetime


def ensure_a_file_extension(p, default_extension):
	basefilename = os.path.splitext(os.path.basename(p))[0]
	basefileext = os.path.splitext(os.path.basename(p))[1]
	if (basefileext == ''):
		filename = basefilename + default_extension
	else:
		filename = basefilename + basefileext
	filename = os.path.join(os.path.dirname(p), filename)
	return filename


def change_file_extension(p, ext):
	basefilename = os.path.splitext(os.path.basename(p))[0]
	filename = basefilename + ext
	filename = os.path.join(os.path.dirname(p), filename)
	return filename


def render_page(templates, template, **data):
	environment = jinja2.Environment(loader=jinja2.FileSystemLoader(templates))
	preprocessed = environment.get_template(template).render(data)
	template = environment.from_string(preprocessed)
	return template.render(data)


def compile_page(page, page_text, templates, config, extra_config):
	if config:
		with open(config) as defaults_file:
			default_config = json.load(defaults_file)
	else:
		default_config = dict()

	if not templates:
		templates = os.getcwd()

	raw_markdown = frontmatter.load(page)
	md = raw_markdown.content

	merged = dict()
	merged.update(default_config)
	merged.update(extra_config)
	merged.update(raw_markdown)

	# mandatory attributes
	if 'canonical' not in merged:
		merged['canonical'] = None

	if 'template' not in merged:
		merged['template'] = 'default.html'

	if 'markdown_extensions' in merged:
		markdown_extensions = merged['markdown_extensions']
	else:
		markdown_extensions = []

	merged['content_raw'] = md

	if 'process_raw' in merged:
		merged['content'] = merged['content_raw']
	else:
		merged['content'] = BeautifulSoup(markdown(md, extensions=markdown_extensions), 'html.parser').prettify()

	if 'canonical' not in raw_markdown.keys():
		page_path = page

		if 'canonical_remove_path_prefix' in merged:
			page_path = page_path[page_path.find(merged['canonical_remove_path_prefix']) + len(merged['canonical_remove_path_prefix']):]

		if 'canonical_relative_path' in merged:
			merged['canonical'] = urllib.parse.urljoin(merged['canonical'], merged['canonical_relative_path'])
		else:
			merged['canonical'] = urllib.parse.urljoin(merged['canonical'], change_file_extension(page_path, '.html'))

	if 'updated' not in merged.keys():
		(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(page)
		merged['updated'] = "%s" % time.ctime(mtime)

	updated = parsedatetime(merged['updated'])
	merged['updated'] = updated.strftime("%a %b %d, %Y")
	if not (updated.hour == 0 and updated.minute == 0 and updated.second == 0):
		merged['updated'] = merged['updated'] + ', ' + updated.strftime("%H:%M:%S")

	merged['year'] = updated.year
	merged['month'] = updated.month
	merged['day'] = updated.day
	merged['templates'] = templates or None
	merged['page'] = os.path.splitext(os.path.basename(page))[0]

	merged['template'] = ensure_a_file_extension(merged['template'], '.html')

	if 'sitestructure' in merged:
		with open(merged['sitestructure'], "r") as f:
			merged['sitestructure'] = json.load(f)

	return merged


def compile(page, page_text, templates, config, extra):
	merged = compile_page(page, page_text, templates, config, extra)
	final = render_page(**merged)
	return final


def sitestructure(config, path, extra):
	"""Read all markdown files and make a site structure file"""
	# no error handling here, because compile_page has it
	entire_site = list()
	for page in glob.iglob(path + '**/*.md', recursive=True):
		merged = compile_page(None, config, page, extra)

		if 'tags' in merged:
			merged['tags'] = [x.strip() for x in merged['tags'].split(',')]

		if 'content_raw' in merged:
			merged['snippet'] = merged['content_raw'][:200] + "..."

		# remote certain elements
		if 'content' in merged:
			del merged['content']

		if 'content_raw' in merged:
			del merged['content_raw']

		if 'templates' in merged:
			del merged['templates']

		entire_site.append(merged)

	return json.dumps(entire_site)
