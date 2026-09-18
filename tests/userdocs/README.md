# User-documentation checks

Run from the repository root:

```sh
python3 scripts/check-userdocs.py
python3 -m unittest discover -s tests/userdocs -v
```

The checker scans root-level user pages, including `fps-reference.md`, and every page in `positions/`. Both FCS user and API pages are integrated, so normal validation uses the strict commands above. The historical cross-workstream option can defer only `api-docs/fcs.md`:

```sh
python3 scripts/check-userdocs.py --allow-pending-api
```

The default is strict. The option reports every deferred reference; it does not suppress other missing pages or anchors. Run `python3 -B scripts/check-api-docs.py` for API schemas, captured responses and executable JavaScript examples.

The checker validates owned Markdown links, local assets, heading fragments, code-fence closure, JSON parsing and Python syntax. Unsupported executable fence languages fail rather than pass unchecked. The user pages currently use text-only formula and signature blocks, not transaction code. API payment validation and malformed HTTP responses belong to the API suite.

Unit tests include negative link, anchor and format fixtures, numerical examples, stored source comparisons and public savings ABI checks. The FCS story tests check canonical framing, navigation hierarchy, underlying FPS identities, cross-page connections and holder journeys. `story-baseline.json` records the starting revision's Markdown anchors and API code-block hashes: moving background material must preserve deep links and must not relabel the tested API examples.

Temporary test trees and numerical illustrations are synthetic, not reported live observations. `source-evidence.json` contains actual retrieved source excerpts, explorer ABIs and indexed token references with their stated provenance. These checks validate documentation; they do not execute Solidity or establish a current deployment's state.
