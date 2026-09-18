# API documentation tests

Run `python3 -B scripts/check-api-docs.py` from the repository root. FCS user pages are integrated, so no sibling worktree or missing-page waiver is needed.

Requirements: Python standard library and Node.js 18+. No package installation, credentials, RPC calls or API network requests are needed.

- `test_examples.py` extracts the exact JavaScript blocks printed in the docs into a temporary directory. `examples.test.mjs` tests those modules, not a duplicate implementation.
- `fixtures/*.body` are unmodified saved public GET responses from 18 September 2026. `fixtures/manifest.json` records source URLs, capture times, HTTP status and SHA-256 hashes. Error responses and inconsistent values are retained as evidence, not silently repaired.
- Synthetic edge cases are labelled in `examples.test.mjs`: mutated recipients/chains/references, malformed responses, decimal variants, stale prices and hypothetical interest. They are not claims about live API observations.
- `routes.json` is a projection of the captured API specification's GET paths. It records the hash of the extracted specification, not a newly generated service response.
- `test_snapshots.py` checks captured schemas, printed JSON provenance and the evidence behind documented endpoint limitations.
- `test_checker.py` verifies that the checker rejects malformed/duplicate-key JSON and missing files/anchors.
- `test_reader_docs.py` checks all ten pages against the editorial manifest, preserves original anchors and fenced examples, validates evidence links and executes the added curl commands with an offline argument recorder.

[Verification evidence](EVIDENCE.md) contains the dated cursor, counter, schema and source observations that support the public guidance. Keep test chronology here rather than in the feature explanations. [Reader coverage](reader-coverage.json) records what each page restores and what inaccurate original claims remain excluded.

Payment examples produce candidates only. Tests do not certify settlement, receipt finality, complete API histories or deployed-contract equivalence. The tests are deterministic documentation regression tests; they do not run transactions or fix the service.
