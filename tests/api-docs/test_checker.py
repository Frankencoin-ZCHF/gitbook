import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class CheckerTests(unittest.TestCase):
    def test_checker_rejects_invalid_json_and_duplicate_keys(self):
        script = ROOT / 'scripts/check-api-docs.py'
        self.assertTrue(script.exists(), 'Missing documentation checker')
        spec = importlib.util.spec_from_file_location('api_checker', script)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.strict_json('{"amount":"1"}'), {'amount': '1'})
        for text in ['{"amount":"1","amount":"2"}', '{"a": NaN}', '{"a": 1, ...}', '{"a": 1 // comment\n}']:
            with self.assertRaises(ValueError):
                module.strict_json(text)

    def test_checker_catches_missing_link_and_anchor(self):
        script = ROOT / 'scripts/check-api-docs.py'
        self.assertTrue(script.exists(), 'Missing documentation checker')
        spec = importlib.util.spec_from_file_location('api_checker', script)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / 'api-docs'
            docs.mkdir()
            (docs / 'README.md').write_text('# API\n[bad](missing.md)\n')
            with self.assertRaises(ValueError):
                module.check_markdown(root)
            (docs / 'README.md').write_text('# API\n[bad](other.md#absent)\n')
            (docs / 'other.md').write_text('# Other\n')
            with self.assertRaises(ValueError):
                module.check_markdown(root)
            (docs / 'README.md').write_text('# API\n[valid](other.md#other)\n```json\n{"ok":true}\n```\n')
            result = module.check_markdown(root)
            self.assertEqual(result['json_examples'], 1)
            self.assertEqual(result['local_links'], 1)


if __name__ == '__main__':
    unittest.main()
