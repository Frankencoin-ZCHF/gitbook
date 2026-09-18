"""Reader-guide structure, preserved examples and offline shell requests.

These guards support, rather than replace, the page-by-page editorial review.
No HTTP calls or wallet transactions occur in this suite.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
BASELINE = json.loads((HERE / 'reader-baseline.json').read_text())
COVERAGE = json.loads((HERE / 'reader-coverage.json').read_text())
spec = importlib.util.spec_from_file_location('api_checker', ROOT / 'scripts/check-api-docs.py')
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def fences(text):
    return re.findall(r'^```[^\n]*\n.*?^```\s*$', text, re.M | re.S)


def prose(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)


class ReaderDocumentation(unittest.TestCase):
    def test_every_api_page_has_reviewed_workflow_coverage(self):
        pages = {str(p.relative_to(ROOT)) for p in (ROOT / 'api-docs').glob('*.md')}
        self.assertEqual(len(pages), 10)
        self.assertEqual(pages, set(BASELINE['pages']))
        self.assertEqual(pages, set(COVERAGE['pages']))
        for name, review in COVERAGE['pages'].items():
            with self.subTest(page=name):
                text = (ROOT / name).read_text()
                self.assertIn(review['workflow_anchor'], checker.anchors(text))
                for field in ('restored', 'preserved', 'not_restored'):
                    self.assertTrue(review[field].strip())
                self.assertNotEqual(hashlib.sha256(text.encode()).hexdigest(),
                                    BASELINE['pages'][name]['base_sha256'])

    def test_original_fences_and_heading_fragments_survive(self):
        for name, baseline in BASELINE['pages'].items():
            with self.subTest(page=name):
                text = (ROOT / name).read_text()
                self.assertFalse(set(baseline['anchors']) - checker.anchors(text))
                observed = [hashlib.sha256(block.strip().encode()).hexdigest()
                            for block in fences(text)]
                # Every original fence must remain byte-for-byte and in order.
                selected = [digest for digest in observed if digest in baseline['fence_sha256']]
                self.assertEqual(selected, baseline['fence_sha256'])

    def test_sampled_observations_stay_out_of_reader_prose(self):
        patterns = [r'\b438[45]\b', r'saved two-page', r'the review .* observed',
                    r'the same review', r'from the same review', r'run .*check-api-docs']
        for name in BASELINE['pages']:
            text = prose((ROOT / name).read_text())
            for pattern in patterns:
                with self.subTest(page=name, pattern=pattern):
                    self.assertNotRegex(text.lower(), pattern)
        analytics = (ROOT / 'api-docs/analytics.md').read_text()
        introduction = analytics.split('### Query a page')[0]
        for field in ('`kind`', '`amount`', '`txHash`'):
            self.assertIn(field, introduction)
        self.assertIn('point-in-time', introduction)
        self.assertIn('not raw on-chain event logs', introduction)
        for claim in ('Every significant event', 'complete financial metrics at that moment',
                      'creates an immutable audit trail', 'Export complete transaction history'):
            self.assertNotIn(claim, analytics)

    def test_moved_evidence_is_linked_and_retains_observations(self):
        text = (HERE / 'EVIDENCE.md').read_text()
        self.assertIn('(EVIDENCE.md)', (HERE / 'README.md').read_text())
        self.assertIn('../tests/api-docs/README.md', (ROOT / 'api-docs/README.md').read_text())
        for observation in ('4385', '4384', '204 characters', '1001', '`NaN`',
                            '35000', '8566.157674440636', 'one pagination step'):
            self.assertIn(observation, text)
        for path in (HERE / 'README.md', HERE / 'EVIDENCE.md'):
            for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', prose(path.read_text())):
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                self.assertTrue(target.is_file(), f'{path.name}: {href}')
                if url.fragment and target.suffix == '.md':
                    self.assertIn(unquote(url.fragment), checker.anchors(target.read_text()))

    def test_added_curl_examples_execute_with_encoded_arguments(self):
        # A local shell function records arguments; it never invokes real curl.
        stub = 'curl() { printf "%s\\0" "$@"; };\n'
        cursor = 'synthetic opaque +/=& cursor'
        routes = json.loads((HERE / 'routes.json').read_text())['get_paths']
        route_patterns = [re.compile('^' + re.sub(r'\\\{[^}]+\\\}', '[^/]+', re.escape(route)) + '$')
                          for route in routes]
        records = []
        for name in BASELINE['pages']:
            for block in re.findall(r'```bash\n(.*?)\n```', (ROOT / name).read_text(), re.S):
                with self.subTest(page=name, block=block):
                    result = subprocess.run(['bash', '--noprofile', '--norc', '-c', stub + block],
                                            env={**os.environ, 'END_CURSOR': cursor},
                                            capture_output=True, check=True, timeout=10)
                    args = result.stdout.decode().split('\0')[:-1]
                    self.assertEqual(args[0], '--fail')
                    urls = [arg for arg in args if arg.startswith('https://')]
                    self.assertEqual(len(urls), 1)
                    url = urlsplit(urls[0])
                    self.assertEqual(url.netloc, 'api.frankencoin.com')
                    self.assertTrue(any(pattern.fullmatch(url.path) for pattern in route_patterns), url.path)
                    params = {}
                    for index, arg in enumerate(args):
                        if arg == '--data-urlencode':
                            key, value = args[index + 1].split('=', 1)
                            params[key] = value
                    if params:
                        self.assertIn('--get', args)
                    records.append((name, url.path, params))
        self.assertEqual(len(records), 8)
        pages = [params for name, _, params in records if name.endswith('/analytics.md')]
        self.assertEqual(pages, [dict(firstItem='false', limit='50'),
                                dict(firstItem='false', limit='50', after=cursor)])
        transfer = [params for name, _, params in records if name.endswith('/transfers.md')]
        self.assertEqual(transfer, [{'reference': '12 months loan'}])


if __name__ == '__main__':
    unittest.main()
