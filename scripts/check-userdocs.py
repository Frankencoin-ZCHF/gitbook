#!/usr/bin/env python3
"""Offline links and source-format checks for user docs. Standard library only.

API pages are read only when resolving a user-doc link, never validated or edited.
Use --allow-pending-api only before integrating the API sibling's fcs.md page.
"""
import argparse
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def targets(text):
    """Parse inline Markdown destinations, including nested/angle parentheses."""
    for match in re.finditer(r'!?\[[^\]\n]*\]\(', text):
        start = match.end()
        if text[start:start + 1] == '<':
            end = text.find('>', start)
            if end != -1:
                yield text[start + 1:end]
            continue
        depth, end = 1, start
        while end < len(text) and depth:
            if text[end] == '(':
                depth += 1
            elif text[end] == ')':
                depth -= 1
            end += 1
        if depth == 0:
            yield text[start:end - 1].split(' "', 1)[0]
    for match in re.finditer(r'(?:src|href)=["\']([^"\']+)["\']', text):
        yield html.unescape(match.group(1))


def anchors(text):
    found, counts = set(), {}
    for line in text.splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)(?:\s+#+)?$', line)
        if match:
            title = re.sub(r'<[^>]*>', '', html.unescape(match.group(1)))
            slug = re.sub(r'[^\w\s-]', '', title.lower()).strip()
            slug = re.sub(r'\s+', '-', slug)
            n = counts.get(slug, 0)
            counts[slug] = n + 1
            found.add(f'{slug}-{n}' if n else slug)
    found.update(re.findall(r'(?:id|name)=["\']([^"\']+)["\']', text))
    return found


def check(root, allow_pending_api=False):
    root = Path(root).resolve()
    errors, pending = [], []
    files = sorted(p for p in root.glob('*.md')) + sorted((root / 'positions').glob('*.md'))
    references = 0
    for path in files:
        text = path.read_text(encoding='utf-8')
        language, fence, block = '', None, []
        for number, line in enumerate(text.splitlines(), 1):
            match = re.match(r'^(`{3,}|~{3,})(.*)$', line)
            if match and fence is None:
                fence, language, block = match[1], match[2].strip(), []
            elif match and fence and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                if language == 'json':
                    try:
                        json.loads('\n'.join(block))
                    except ValueError as exc:
                        errors.append(f'{path.name}:{number}: invalid JSON: {exc}')
                elif language == 'python':
                    try:
                        compile('\n'.join(block), str(path), 'exec')
                    except SyntaxError as exc:
                        errors.append(f'{path.name}:{number}: invalid Python: {exc}')
                elif language not in ('', 'text', 'json', 'python'):
                    errors.append(f'{path.name}:{number}: untested fence language {language}')
                fence = None
            elif fence:
                block.append(line)
        if fence:
            errors.append(f'{path.name}: unclosed code fence')
        if '\u2014' in text:
            errors.append(f'{path.name}: em dash in user documentation')
        if re.search(r'\bTODO\b', text):
            errors.append(f'{path.name}: unfinished TODO')
        prose = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        for target in targets(prose):
            url = urlsplit(target)
            if url.scheme or target.startswith('//'):
                continue
            references += 1
            relative = unquote(url.path).replace('\\_', '_')
            dest = (path.parent / relative).resolve() if relative else path
            if dest.is_dir():
                dest = dest / 'README.md'
            try:
                name = dest.relative_to(root).as_posix()
            except ValueError:
                errors.append(f'{path.name}: target escapes repository: {target}')
                continue
            if not dest.exists():
                if allow_pending_api and name == 'api-docs/fcs.md':
                    pending.append(f'{path.relative_to(root)}: {target}')
                else:
                    errors.append(f'{path.relative_to(root)}: missing {target}')
            elif url.fragment and dest.suffix == '.md':
                if unquote(url.fragment) not in anchors(dest.read_text(encoding='utf-8')):
                    errors.append(f'{path.relative_to(root)}: missing anchor {target}')
    return {'files': len(files), 'local_references': references, 'errors': errors, 'pending': pending}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--allow-pending-api', action='store_true')
    args = parser.parse_args()
    report = check(args.root, args.allow_pending_api)
    print(json.dumps(report, indent=2))
    return bool(report['errors'])


if __name__ == '__main__':
    raise SystemExit(main())
