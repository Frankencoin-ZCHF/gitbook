"""Execute the JavaScript printed in the guide, not a second implementation."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class DocumentationExamples(unittest.TestCase):
    def test_javascript_examples(self):
        with tempfile.TemporaryDirectory(prefix="api-doc-examples-") as directory:
            examples = {}
            for page in (ROOT / "api-docs").glob("*.md"):
                blocks = re.findall(r"```javascript\n(.*?)\n```", page.read_text(), re.S)
                if blocks:
                    examples[page.stem] = "\n".join(blocks)
                    Path(directory, page.stem + ".mjs").write_text("\n".join(blocks))
            self.assertIn("README", examples, "Missing executable shared validation example")
            result = subprocess.run(
                ["node", "--test", str(ROOT / "tests/api-docs/examples.test.mjs")],
                env={**os.environ, "EXAMPLE_DIR": directory}, text=True, capture_output=True,
            )
            print(result.stdout, end="")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
