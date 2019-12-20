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


def compile_page(templates, config, page, extra):
	extra_config = dict()
	if extra:
		for item in extra:
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

	merged['content_raw'] = md
	merged['content'] = BeautifulSoup(markdown(md, extensions=markdown_extensions), 'html.parser').prettify()

	if 'canonical' not in raw_markdown.keys():
		page_path = page

		if 'canonical_remove_path_prefix' in merged:
			page_path = page_path[page_path.find(merged['canonical_remove_path_prefix']) + len(merged['canonical_remove_path_prefix']):]

		if 'canonical_relative_path' in merged:
			merged['canonical'] = urllib.parse.urljoin(default_config['canonical'], merged['canonical_relative_path'])
		else:
			merged['canonical'] = urllib.parse.urljoin(default_config['canonical'], change_file_extension(page_path, '.html'))

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
	merged['template'] = change_file_extension(merged['template'], '.html')

	if 'sitestructure' in merged:
		with open(merged['sitestructure'], "r") as f:
			merged['sitestructure'] = json.load(f)

	return merged


def compile(templates, config, page, extra):
	merged = compile_page(templates, config, page, extra)
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
