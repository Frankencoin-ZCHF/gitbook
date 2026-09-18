"""Offline documentation regressions; temporary trees are synthetic fixtures."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('checker', ROOT / 'scripts/check-userdocs.py')
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class LinkTests(unittest.TestCase):
    def test_missing_local_target_is_an_error(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'README.md').write_text('# Example\n[Missing](missing.md)\n')
            report = checker.check(root)
            self.assertTrue(any('missing.md' in e for e in report['errors']))


    def test_markup_links_assets_and_anchors(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'asset (1).svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            (root / 'page.md').write_text('# A page\n## Real anchor\n')
            page = root / 'README.md'
            page.write_text('# Main\n[Good](page.md#real-anchor)\n'
                            '![Asset](<asset (1).svg>)\n'
                            '<img src="asset (1).svg" alt="asset">\n'
                            '[Remote](https://example.org/path_(part))\n')
            self.assertEqual([], checker.check(root)['errors'])
            page.write_text('# Main\n[Bad](page.md#missing-anchor)\n'
                            '<img src="absent.png" alt="missing">\n')
            errors = checker.check(root)['errors']
            self.assertTrue(any('missing-anchor' in e for e in errors))
            self.assertTrue(any('absent.png' in e for e in errors))


class FormatTests(unittest.TestCase):
    def test_malformed_examples_and_unclosed_fence_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'README.md'
            for body in ['# Page\n```json\n{"a": }\n```\n', '# Page\n```text\nunclosed\n']:
                page.write_text(body)
                self.assertTrue(checker.check(root)['errors'])
            page.write_text('# Page\n```json\n{"a": 1}\n```\n')
            self.assertEqual([], checker.check(root)['errors'])

    def test_only_named_cross_stream_target_can_be_pending(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'README.md'
            page.write_text('# Page\n[FCS](api-docs/fcs.md)\n')
            self.assertTrue(checker.check(root)['errors'])
            self.assertFalse(checker.check(root, True)['errors'])
            self.assertTrue(checker.check(root, True)['pending'])
            page.write_text('# Page\n[Other](api-docs/missing.md)\n')
            self.assertTrue(checker.check(root, True)['errors'])


if __name__ == '__main__':
    unittest.main()
