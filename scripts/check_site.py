#!/usr/bin/env python3
"""Check a Jekyll build for broken internal links and local assets (stdlib only)."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = set()
        self.duplicates = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get('id')
        if ident:
            if ident in self.ids:
                self.duplicates.add(ident)
            self.ids.add(ident)
        for attr in ('href', 'src', 'poster'):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == 'meta' and attrs.get('name') in ('msapplication-TileImage', 'msapplication-config'):
            self.refs.append(attrs['content'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', default='_site')
    parser.add_argument('--base-url', default='https://caoac.github.io')
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    if not (root / 'index.html').is_file():
        parser.error('Build the site first: bundle exec jekyll build --safe')
    base = args.base_url.rstrip('/') + '/'
    origin = urlsplit(base)
    base_path = origin.path.rstrip('/')
    pages = {p: Page(p.read_text()) for p in root.rglob('*.html')}
    errors = set()
    checked = 0

    def check(source, ref):
        nonlocal checked
        resolved = urlsplit(urljoin(urljoin(base, source.relative_to(root).as_posix()), ref))
        if resolved.scheme not in ('http', 'https') or resolved.netloc != origin.netloc:
            return
        checked += 1
        path = unquote(resolved.path)
        if '//' in path:
            errors.add(f'{source.relative_to(root)}: double slash in {ref}')
        if base_path and not (path == base_path or path.startswith(base_path + '/')):
            errors.add(f'{source.relative_to(root)}: URL escapes base path: {ref}')
            return
        path = path[len(base_path):].lstrip('/')
        target = root / path
        candidates = [target / 'index.html'] if path.endswith('/') or not path else [target, target / 'index.html', root / (path + '.html')]
        target = next((p for p in candidates if p.is_file()), None)
        if target is None:
            errors.add(f'{source.relative_to(root)}: missing {ref}')
        elif resolved.fragment and target in pages:
            fragment = unquote(resolved.fragment)
            if fragment not in pages[target].ids:
                errors.add(f'{source.relative_to(root)}: missing anchor {ref}')

    for source, page in pages.items():
        for ident in page.duplicates:
            errors.add(f'{source.relative_to(root)}: duplicate id {ident}')
        for ref in page.refs:
            check(source, ref)
    for source in root.rglob('*.css'):
        for ref in re.findall(r'url\(\s*[\'\"]?([^\)\'\"\s]+)', source.read_text()):
            check(source, ref)
    manifest = root / 'images/manifest.json'
    if manifest.is_file():
        for icon in json.loads(manifest.read_text()).get('icons', []):
            check(manifest, icon['src'])
    for source in (root / 'sitemap.xml', root / 'images/browserconfig.xml'):
        if source.is_file():
            for element in ElementTree.parse(source).iter():
                if element.tag.endswith('}loc') and element.text:
                    check(source, element.text)
                if element.get('src'):
                    check(source, element.get('src'))
    if errors:
        print('\n'.join(sorted(errors)), file=sys.stderr)
        return 1
    print(f'PASS: {len(pages)} HTML pages, {checked} internal link/asset references; no missing targets, duplicate IDs, or double-slash paths.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
