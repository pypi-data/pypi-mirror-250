#!/usr/bin/env python3
# Advert generator from web feeds
# Copyright (C) 2022, 2024  Nguyễn Gia Phong
# Copyright (C) 2023  Ngô Ngọc Đức Huy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__version__ = '1.0.0'

from argparse import ArgumentParser, FileType, HelpFormatter
from asyncio import CancelledError, TaskGroup, gather, open_connection, run
from collections import namedtuple
from datetime import datetime
from email.utils import parsedate_to_datetime
from http.client import HTTPResponse
from importlib import import_module
from io import BytesIO
from operator import attrgetter
from pathlib import Path
from re import compile as regex
from sys import stdin, stdout
from textwrap import shorten
from traceback import print_exception
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from warnings import warn
from xml.etree.ElementTree import (fromstring as parse_xml,
                                   tostring as unparse_xml)

REQUEST = 'GET {} HTTP/1.0\r\nHost: {}\r\n\r\n'
HTML_TAG = regex('<.+?>')

Advert = namedtuple('Advert', ('source_title', 'source_link',
                               'title', 'link', 'time', 'summary'))

# Show only message in warnings.
import_module('warnings').formatwarning = 'Warning: {}\n'.format


class GNUHelpFormatter(HelpFormatter):
    """Help formatter for ArgumentParser following GNU Coding Standards."""

    def add_usage(self, usage, actions, groups, prefix='Usage: '):
        """Substitute 'Usage:' for 'usage:'."""
        super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        """Substitute 'Options:' for 'options:'."""
        super().start_section(heading.capitalize())


def read_urls(path):
    """Read newline-separated URLs from given file path."""
    return Path(path).read_text().splitlines()


class BytesSocket:
    """Duck socket for HTTPResponse."""
    def __init__(self, response):
        self.bytes = response

    def makefile(self, mode, *args, **kwargs):
        """Return a bytes stream."""
        assert mode == 'rb'
        return BytesIO(self.bytes)


def parse_rss_item(xml):
    """Parse given RSS item."""
    time = datetime.fromtimestamp(0)
    description = ''
    for child in xml:
        if child.tag == 'title':
            title = child.text
        elif child.tag == 'link':
            link = child.text
        elif child.tag == 'pubDate':
            time = parsedate_to_datetime(child.text)
        elif child.tag == 'description':
            description = child.text
        elif child.tag.endswith('}encoded') and not description:
            description = child.text
    if not description:
        description = xml.text
    return title, link, time, description


def parse_rss(xml, title):
    """Parse given RSS feed."""
    items = []
    for child in xml:
        if child.tag == 'title':
            title = child.text
        elif child.tag == 'link':
            link = child.text
        elif child.tag == 'item':
            items.append(parse_rss_item(child))
    return title, link, items


def parse_atom_entry(xml):
    """Parse given Atom entry."""
    time = datetime.fromtimestamp(0)
    summary = ''
    for child in xml:
        if child.tag.endswith('Atom}title'):
            title = child.text
        elif child.tag.endswith('Atom}link'):
            rel = child.attrib.get('rel')
            if rel == 'alternate' or not rel: link = child.attrib['href']
        elif child.tag.endswith('Atom}published'):
            iso = child.text.replace('Z', '+00:00')  # normalized
            time = datetime.fromisoformat(iso)
        elif child.tag.endswith('Atom}summary'):
            summary = child.text
        elif child.tag.endswith('Atom}content') and not summary:
            if child.attrib.get('type') == 'xhtml':
                assert len(child) == 1 and child[0].tag.endswith('xhtml}div')
                summary = unparse_xml(child[0]).decode()
            else:
                summary = child.text
    return title, link, time, summary


def parse_atom(xml, title, link):
    """Parse given Atom feed."""
    entries = []
    for child in xml:
        if child.tag.endswith('Atom}title'):
            title = child.text
        elif child.tag.endswith('Atom}link'):
            rel = child.attrib.get('rel')
            if rel == 'alternate' or not rel: link = child.attrib['href']
        elif child.tag.endswith('Atom}entry'):
            entries.append(parse_atom_entry(child))
    return title, link, entries


async def fetch(raw_url):
    """Fetch web feed from given URL and return it parsed."""
    url = urlsplit(raw_url)
    if url.scheme == 'https':
        reader, writer = await open_connection(url.hostname, 443, ssl=True)
    elif url.scheme == 'http':
        reader, writer = await open_connection(url.hostname, 80)
    else:
        raise ValueError(f'unsupported URL scheme: {raw_url}')
    try:
        writer.write(REQUEST.format(f"{url.path or '/'}?{url.query}",
                                    url.hostname).encode())
        response = HTTPResponse(BytesSocket(await reader.read()))
    except CancelledError:
        return None  # silence propagation
    finally:
        writer.close()

    response.begin()
    with response:
        if response.status >= 400:
            raise HTTPError(raw_url, response.status,
                            f'{response.reason}: {raw_url}',
                            response.getheaders(), response)
        if response.status >= 300:
            location = urljoin(raw_url, response.getheader('Location'))
            warn(f'{raw_url} redirected to {location}')
            return await fetch(location)
        if response.status >= 200:
            try:
                xml = parse_xml(response.read())
            except SyntaxError as e:
                raise ValueError(f'malformed XML at {raw_url}') from e
            if xml.tag == 'rss':
                assert xml[0].tag == 'channel'
                src_title, src_link, items = parse_rss(xml[0], url.hostname)
            elif xml.tag.endswith('Atom}feed'):
                src_title, src_link, items = parse_atom(xml, url.hostname,
                                                        raw_url)
            else:
                raise ValueError(f'unsupported feed format at {raw_url}')
            return (Advert(src_title, urljoin(raw_url, src_link),
                           title, urljoin(raw_url, link),
                           time.astimezone(None), summary)
                    for title, link, time, summary in items)
        raise HTTPError(raw_url, response.status,
                        f'{response.reason}: {raw_url}',
                        response.getheaders(), response)


async def fetch_all(urls, strict):
    """Fetch all given URLs asynchronously and return them parsed.

    If in strict mode, abort when encounter the first error.
    """
    if strict:
        async with TaskGroup() as group:
            tasks = tuple(group.create_task(fetch(url)) for url in urls)
        return (task.result() for task in tasks)
    else:
        feeds, exceptions = [], []
        for result in await gather(*map(fetch, urls), return_exceptions=True):
            if isinstance(result, BaseException):
                exceptions.append(result)
            else:
                feeds.append(result)
        if exceptions:
            warn('some web feed(s) have been skipped')
            print_exception(ExceptionGroup("ignored errors", exceptions))
        return feeds


def select(n, ads):
    """Return n most recent ads from given iterable."""
    return sorted(ads, key=attrgetter('time'), reverse=True)[:n]


def truncate(ad, summary_length):
    """Return ad with truncated summary, whose HTML tags a stripped."""
    return ad._replace(summary=shorten(HTML_TAG.sub('', ad.summary),
                                       summary_length, placeholder='…'))


def main():
    """Run command-line program."""
    parser = ArgumentParser(prog='fead', usage='%(prog)s [OPTION]...',
                            description='Generate adverts from web feeds.',
                            epilog='Any use of -f before -F is ignored.',
                            formatter_class=GNUHelpFormatter,
                            allow_abbrev=False)
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    parser.add_argument('-F', '--feeds', metavar='PATH',
                        type=read_urls, default=[],
                        help='file containing newline-separated web feed URLs')
    parser.add_argument('-f', '--feed', metavar='URL',
                        action='append', dest='feeds',
                        help='addtional web feed URL (multiple use)')
    parser.add_argument('-s', '--strict', action='store_true',
                        help='abort when fail to fetch or parse a web feed')
    parser.add_argument('-n', '--count', metavar='N', type=int, default=3,
                        help='maximum number of ads in total (default to 3)')
    parser.add_argument('-p', '--per-feed', metavar='N', type=int, default=1,
                        help='maximum number of ads per feed (default to 1)')
    parser.add_argument('-l', '--length', metavar='N',
                        dest='len', type=int, default=256,
                        help='maximum summary length (default to 256)')
    parser.add_argument('-t', '--template', metavar='PATH',
                        type=FileType('r'), default=stdin,
                        help='template file (default to stdin)')
    parser.add_argument('-o', '--output', metavar='PATH',
                        type=FileType('w'), default=stdout,
                        help='output file (default to stdout)')
    args = parser.parse_args()

    template = args.template.read()
    args.template.close()
    for ad in select(args.count,
                     (ad for feed in run(fetch_all(args.feeds, args.strict))
                      for ad in select(args.per_feed, feed))):
        args.output.write(template.format(**truncate(ad, args.len)._asdict()))
    args.output.close()


if __name__ == '__main__': main()
