#!/usr/bin/env python3
"""Offline API documentation checks. Python standard library and Node.js 18+ only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result

    def invalid(value):
        raise ValueError(f'Invalid JSON constant: {value}')

    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)


def anchors(text):
    found, counts = set(), {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        heading = re.sub(r'[`*_]', '', heading).lower()
        slug = re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')
        count = counts.get(slug, 0)
        found.add(slug + (f'-{count}' if count else ''))
        counts[slug] = count + 1
    found.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    return found


def check_markdown(root, sibling_root=None):
    report = {'pages': 0, 'json_examples': 0, 'javascript_modules': 0,
              'local_links': 0, 'sibling_links': []}
    for page in sorted((root / 'api-docs').glob('*.md')):
        report['pages'] += 1
        text = page.read_text()
        if text.count('```') % 2:
            raise ValueError(f'Unclosed code fence: {page}')
        if '\u2014' in text:
            raise ValueError(f'Em dash: {page}')
        for block in re.findall(r'```json\n(.*?)\n```', text, re.S):
            strict_json(block)
            report['json_examples'] += 1
        blocks = re.findall(r'```javascript\n(.*?)\n```', text, re.S)
        report['javascript_modules'] += bool(blocks)
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', prose):
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            report['local_links'] += 1
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page.resolve()
            if not target.exists() and sibling_root:
                relative = target.relative_to(root.resolve())
                if str(relative) in {'fcs.md', 'fcs-migration.md'}:
                    target = sibling_root / relative
                    report['sibling_links'].append(str(relative))
            if not target.is_file():
                raise ValueError(f'Missing local link: {page.name}: {href}')
            if parts.fragment and target.suffix == '.md':
                if unquote(parts.fragment) not in anchors(target.read_text()):
                    raise ValueError(f'Missing anchor: {page.name}: {href}')
    return report


def check_fixtures(root):
    fixtures = root / 'tests/api-docs/fixtures'
    manifest = strict_json((fixtures / 'manifest.json').read_text())
    names = set()
    for row in manifest:
        if row['file'] in names:
            raise ValueError('Duplicate fixture in manifest')
        names.add(row['file'])
        data = (fixtures / row['file']).read_bytes()
        if hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError(f'Fixture checksum mismatch: {row["file"]}')
        strict_json(data.decode())
    files = {p.name for p in fixtures.glob('*.body')}
    if files != names:
        raise ValueError('Fixture manifest coverage differs from files')
    return len(names)


def check_routes(root):
    snapshot = strict_json((root / 'tests/api-docs/routes.json').read_text())
    available = set(snapshot['get_paths'])
    documented = set()
    for page in (root / 'api-docs').glob('*.md'):
        text = page.read_text()
        routes = re.findall(r'\| `(/[^`]+)` \|', text)
        routes += re.findall(r'`GET (/[^`\s]+)`', text)
        for route in routes:
            normal = re.sub(r':([A-Za-z][A-Za-z0-9]*)', r'{\1}', route)
            if normal not in available:
                raise ValueError(f'Unknown documented route: {page.name}: {route}')
            documented.add(normal)
    return len(documented)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sibling-root', type=Path,
                        help='Read only agreed FCS root pages from the sibling worktree until integration')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    report = check_markdown(root, args.sibling_root)
    if report['pages'] != 10 or report['javascript_modules'] != 4:
        raise ValueError(f'Unexpected API page/example coverage: {report}')
    report['captured_fixtures'] = check_fixtures(root)
    report['documented_get_routes'] = check_routes(root)
    print(json.dumps(report, indent=2), flush=True)
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                             '-s', 'tests/api-docs', '-v'], cwd=root)
    return result.returncode


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
