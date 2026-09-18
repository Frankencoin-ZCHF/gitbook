# API verification evidence

This file preserves verification details removed from reader-facing API pages during the editorial revision from `56555dce5a57a674fcc9046caeee548f266f36d6`. It is a record of evidence and its limits, not a statement of current service health. The original instructional comparison is `598be69c450550a5b64d3c01a242901cf1d23fcb`.

The public GET responses were captured on 18 September 2026 against API version `0.4.2`. [The fixture manifest](fixtures/manifest.json) records each URL, capture time, HTTP status and SHA-256 hash. Raw bodies are unchanged. [The route snapshot](routes.json) preserves the captured specification's GET paths and extracted-specification hash. See the [test guide](README.md) for commands and synthetic-case boundaries.

## Analytics pagination and financial data

- [Fixture 22](fixtures/22.body) contains the first one-row transaction-log page, with count `4385`. [Fixture 36](fixtures/36.body) contains the next page, with count `4384`. The second request used the first response's full `pageInfo.endCursor`; the shortened URL in the manifest is a display artefact, not the cursor to replay.
- Comparing stored bytes shows distinct end cursors. The first cursor has 204 characters and contains no literal `...`. Do not infer equality from redacted tool displays. `test_analytics_units_and_cursor_limitations` checks these facts directly from the saved responses.
- This establishes one pagination step, not full-history traversal. No exhaustive export was certified. Public guidance therefore explains cursor handling, overlapping rows, stalled traversal and independent reconciliation without presenting this sample as a pagination guarantee.
- [Fixture 23](fixtures/23.body), newly copied unchanged from the original review's saved response, contains 818 daily rows despite `limit=1`. The manifest now contains the original 31 fixtures plus this response. Its timestamps are Unix seconds and match the `date` fields, despite a milliseconds label in the controller's schema description. Tests check all dates against the stored timestamps.
- Pinned [analytics source excerpts](reader-source-evidence.json) establish a fixed daily-log query limit of 1000, ascending timestamp order, no controller pagination parameters, transaction page size 50, opaque `after` forwarding and the mixed CSV/pagination response. The service passes daily timestamps through unchanged; captured response units take precedence over the contradictory schema description. Public guidance explains local date selection and checking the last available date, not sampled counts.
- The same service derives some earnings categories rather than summing receipt-level events; for example, it computes `positionProposalFees` as a fixed amount times the number of original positions. The guide describes the endpoint as a breakdown, not an itemised ledger.
- [Fixture 21](fixtures/21.body) has `minterProposalFees: 25000`, meaning 25,000 ZCHF, not base units. [Fixture 20](fixtures/20.body) contains already scaled exposure metrics. Transaction-log monetary quantities in fixture 22 are raw strings instead.
- The saved transaction schema has `totalEquity`, `totalSavings`, `fpsTotalSupply`, `fpsPrice`, `realizedNetEarnings` and `earningsPerFPS`. It does not have total ZCHF supply, V1/V2 minting totals or interest rates. Original prose claiming complete financial metrics, every significant event or an immutable API audit trail was not restored.

## Transfer dates, exact filters and counter inconsistencies

- [Fixture 18](fixtures/18.body) records HTTP 200 with an Apollo/GraphQL error containing `NaN` after numeric Unix-second `start`/`end` query strings. [Fixture 37](fixtures/37.body) records an array for ISO-date boundaries. Source inspection established inclusive start and exclusive end after conversion to seconds. This is point-in-time evidence of a parsing defect, not a claim that the service is currently failing.
- [Fixture 49](fixtures/49.body), queried with `reference=12 months`, is empty. [Fixture 50](fixtures/50.body), queried with `reference=12 months loan`, contains the exact match. The example keeps exact, case-sensitive matching and uses `URLSearchParams`.
- The counter in [fixture 16](fixtures/16.body) is `1000`, yet [fixture 28](fixtures/28.body) contains count `1001`; [fixture 51](fixtures/51.body) later reports counter `0`. [Fixture 27](fixtures/27.body) includes a null list row. These observations do not supply a reliable high-water mark or a payment cursor.
- [Fixture 29](fixtures/29.body) includes seven rows, a same-chain `targetChain` sentinel of `"0"` and nonzero CCIP selectors beyond JavaScript's safe integer range. A selector is not an EIP-155 chain ID or destination settlement proof.
- Source inspection found a 100-row history cap with no exposed cursor. No complete transfer-history traversal was certified. The candidate matcher preserves recipient, payer, source-chain, exact-reference and integer-amount checks; it never establishes settlement.

## FCS identity, quotes and source boundary

- The public FCS JSON examples are exactly [fixture 33](fixtures/33.body) and [fixture 34](fixtures/34.body), not current quotes or synthetic responses. [Fixture 3](fixtures/03.body) reports underlying FPS at `0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2`, with supply `8566.157674440636`; the FCS supply in fixture 33 differs. Equal reference ask/bid values do not make the tokens or supplies interchangeable.
- FCS API conversions and fallback behaviour come from [service source at `9013d8f`](https://github.com/Frankencoin-ZCHF/frankencoin-api/blob/9013d8fadf2bcc251d236c78328958ebcfbe1c26/src/modules/fcs/fcs.service.ts). Failed reads substitute `0` for `bid()` and `1` for `currentDiscount(0)`; public guidance retains this ambiguity and recommends contract reads for quotes.
- Contract mechanics refer to the [ChainSecurity FPS2 report](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf), final V3 at `c1f229e3b26050367aafcb55da294342b4cae382`. The report calls the wrapper FPS2. It is not proof of deployed bytecode equivalence, and captured API deployment fields are not audit conclusions. Existing [source-boundary evidence](../userdocs/source-evidence.json) is unchanged.

## Savings modules and rates

- [Fixture 5](fixtures/05.body) has mainnet modules `0x27d9ad987bde08a0d083ef7e0e4043c857a17b38` and `0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae`, with rates `35000` and `10000` PPM, or 3.5% and 1% annual simple rates. These are dated observations, not recommended deployment addresses or current rates.
- [Fixture 6](fixtures/06.body), printed unchanged in the savings guide, nests an account by chain and module. [Fixture 8](fixtures/08.body) provides leadrate information. These support explicit module selection, root-level aggregate fields and PPM conversion.
- Contract-interface explanations refer to [AbstractSavings at `8b4c4ab`](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/savings/AbstractSavings.sol). Older interfaces differ. The projection tests use hypothetical unchanged rates and eligible time, not live accrued-interest calculations or transaction tests.

## Challenges, ecosystem data and prices

- [Fixture 14](fixtures/14.body) includes `Success` challenges with `acquiredCollateral="0"`. [Fixture 15](fixtures/15.body) uses full bid IDs, not challenge IDs, as mapping keys. [Fixture 52](fixtures/52.body) is an empty current-prices map. These facts do not establish the full status-label derivation or future auction availability.
- V2 challenge mechanics refer to [MintingHubV2 at `8b4c4ab`](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/v2/MintingHubV2.sol). The second-phase purchase executes with the bid; it is not a batch settlement at auction end. The explanation is not applied to all V1 records.
- [Fixture 24](fixtures/24.body) includes denied minter proposals and has no active/deprecated/proposed enum or version field. [Fixture 25](fixtures/25.body) includes collateral with 0, 6, 8 and 18 decimals. Neither list proves current authorisation or a collateral whitelist.
- [Fixture 9](fixtures/09.body) uses lowercase address keys, CHF and USD prices, millisecond timestamps, sources including `defillama`, `thegraph`, `custom` and `null`, and missing-price indicators. [Fixture 11](fixtures/11.body) groups positions by owner. The exact-rational example tests preserve chain/token/decimal matching and same-currency valuation.
- No complete free-float ratio formula or market-chart quote denomination was established by the reviewed schema. Those remain integration questions, not invented defaults or generic healthy-ratio bands.

## Editorial and example regression checks

[The reader baseline](reader-baseline.json) records the ten-page manifest, all pre-edit heading fragments and original fenced-block hashes. Each original API page was read in full at both comparison revisions where it existed; FCS is absent from `598be69` and was reviewed against the implemented API page and pinned source boundary instead.

[The editorial tests](test_reader_docs.py) check manifest coverage, preserved blocks and anchors, local evidence links, separation of sampled observations from public prose and the added shell examples. Shell examples execute with a local argument-recording replacement for `curl`; this tests command syntax, routes and URL encoding without issuing network requests. They do not certify service responses. Existing Node tests continue to execute the exact JavaScript printed in Markdown against captured responses and labelled synthetic edge cases.

The explanatory pass is a human review against the [page-by-page coverage record](reader-coverage.json), not a claim that word-presence tests prove prose quality. No live writes, transaction execution, settlement verification or exhaustive endpoint recapture form part of this revision.
