# This file was based on HTMLark
# https://github.com/BitLooter/htmlark/blob/master/htmlark.py
# The code was lifted and placed here with modifications
# The original code came with the MIT license, which allows for the code to be
# modified and merged.
#
# The original license follows
#######################
# The MIT License (MIT)
#
# Copyright (c) 2015 David Powell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from bs4 import BeautifulSoup
import urllib.parse
import base64
import mimetypes
from requests import get as requests_get


def make_data_uri(mimetype: str, data: bytes) -> str:
	mimetype = '' if mimetype is None else mimetype
	if mimetype in ['', 'text/css', 'application/javascript']:
		encoded_data = urllib.parse.quote(data.decode())
	else:
		mimetype = mimetype + ';base64'
		encoded_data = base64.b64encode(data).decode()
	return "data:{},{}".format(mimetype, encoded_data)


def _get_resource(resource_url):
	mimetype = None
	resource_url_parsed = urllib.parse.urlparse(resource_url)
	if resource_url_parsed.scheme in ['http', 'https']:
		request = requests_get(resource_url)
		data = request.content
		if 'Content-Type' in request.headers:
			mimetype = request.headers['Content-Type']
	else:
		with open(resource_url, 'rb') as f:
			data = f.read()

	if mimetype is None:
		mimetype, _ = mimetypes.guess_type(resource_url)

	return mimetype, data


def archive(page_path, page_text, **kwargs):
	ignore_images = False
	ignore_css = False
	ignore_js = False
	ignore_errors = kwargs['ignore_errors'] if 'ignore_errors' in kwargs else False

	soup = BeautifulSoup(page_text, features="html.parser")

	tags = []

	# Gather all the relevant tags together
	if not ignore_images:
		tags += soup('img')
	if not ignore_css:
		csstags = soup('link')
	for css in csstags:
		if 'stylesheet' in css['rel']:
			tags.append(css)
	if not ignore_js:
		scripttags = soup('script')
		for script in scripttags:
			if 'src' in script.attrs:
				tags.append(script)

	for tag in tags:
		tag_url = tag['href'] if tag.name == 'link' else tag['src']
		try:
			tag_url_parsed = urllib.parse.urlparse(tag_url)
			if tag_url_parsed.scheme in ['http', 'https']:
				fullpath = tag_url
			else:
				directory = os.path.dirname(os.path.realpath(page_path))
				fullpath = directory + '/' + tag_url
				fullpath = os.path.normpath(fullpath)

			tag_mime, tag_data = _get_resource(fullpath)
			encoded_resource = make_data_uri(tag_mime, tag_data)
		except:
			if not ignore_errors:
				raise
			else:
				continue

		if tag.name == 'link':
			tag['href'] = encoded_resource
		else:
			tag['src'] = encoded_resource

	return str(soup)
