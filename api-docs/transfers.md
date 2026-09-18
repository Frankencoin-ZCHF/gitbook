# Transfers API

Read indexed ZCHF transfers carrying reference messages. These GET endpoints do not send payments, establish finality, or prove that an invoice has been paid. Ordinary ERC-20 transfers without references are outside this dataset.

## Endpoints and response shapes

| GET path | Response | Boundary |
| --- | --- | --- |
| `/transfer/reference/list` | `{num, list}` | Cached observations, not a complete ledger or reliable cursor |
| `/transfer/reference/counter` | Number | Not a reliable high-water mark |
| `/transfer/reference/by/count/:count` | One record or an error | A missing record is not proof of no transfer |
| `/transfer/reference/by/from/:from` | Array | Cached outgoing matches |
| `/transfer/reference/by/to/:to` | Array | Cached incoming matches |
| `/transfer/reference/history/by/from/:from` | Array | Indexed history, capped at 100 rows in inspected source, no exposed cursor |
| `/transfer/reference/history/by/to/:to` | Array | Same cap and completeness limitation |

The opposite-party filter is `to` on sender routes and `from` on recipient routes. `reference` is an **exact, case-sensitive** match, not substring search. Encode query parameters with `URLSearchParams`. Do not interpolate reference text into a URL. References are public, untrusted text; render them as text, not HTML, and never include secrets.

### Time ranges and errors

Use ISO dates or explicit UTC ISO timestamps for history `start` and `end`. Inspected source applies an inclusive start and exclusive end after converting the dates to seconds. Whole-second UTC boundaries avoid rounding ambiguity.

```text
GET /transfer/reference/history/by/from/0x963eC454423CD543dB08bc38fC7B3036B425b301?start=2024-01-01T00%3A00%3A00.000Z&end=2025-01-01T00%3A00%3A00.000Z
```

The review on 18 September 2026 observed numeric Unix-second query strings returning HTTP 200 with an Apollo/GraphQL `NaN` error, while ISO-date strings returned an array. This is an upstream parsing defect, not repaired by these docs. Always check both HTTP status and payload shape. An error, timeout, null row or malformed response means **data unavailable**, never “no payments”. An empty valid array means no indexed matches in that response, not a complete absence of payments.

### Counter and completeness limitations

The same review observed counter `1000` while count `1001` existed, a null entry in the list, and a later counter of `0`. Do not use counter increases, ordering, or `count > lastCount` as a notification/payment cursor. Latest caches and capped history can omit records. There is no documented transfer-history pagination contract; splitting time ranges alone cannot prove completeness when 100 events share a boundary.

For a complete ledger, use a separately validated indexer or the relevant contracts' logs via an RPC with explicit block-range pagination, persisted checkpoints, reorg handling and reconciliation against receipts. Verify each supported chain, contract deployment block and event ABI. Do not label an API-only export complete.

## Record fields

| Field | Type and meaning |
| --- | --- |
| `amount` | Decimal integer string in ZCHF base units (18 decimals) |
| `chainId` | Number: source EIP-155 chain ID |
| `count`, `created` | Observed decimal integer strings; Swagger also describes numbers. `created` is Unix seconds. Preserve count without floating-point coercion |
| `from`, `sender`, `to` | Addresses; `from` and original `sender` can differ. Validate before case-normalized comparison |
| `reference` | Exact public reference string, possibly empty |
| `targetChain` | Decimal string: `0` is the same-chain sentinel; otherwise a CCIP chain selector, **not** an EIP-155 ID |
| `txHash` | Full source-chain transaction hash |

Keep CCIP selectors as strings or `BigInt`; some exceed JavaScript's safe integer range. Resolve nonzero selectors against the maintained CCIP configuration for the relevant deployment. Never compare `chainId !== targetChain` to detect destination settlement. A source-chain reference event does not establish receipt on the destination chain.

## Invoice integration boundary

The former invoice-paid and counter-polling examples have been removed. A reference/amount match is only a **candidate for verification**. This API record does not supply the token-emitting address, log index, receipt success, confirmations, or destination settlement proof needed to authorize delivery.

Before crediting a payment:

1. Require the intended recipient, payer policy, exact invoice identifier, chain, token contract and integer amount. Reject underpayment; handle partial/overpayments under an explicit business policy.
2. Fetch and validate the successful transaction receipt on the expected chain. Decode the correct contract's reference and token events and bind them to each other; matching a hash alone is insufficient.
3. Apply a chain-specific finality/reorg policy. For bridges, verify destination token, recipient and settlement independently.
4. Deduplicate by `(chainId, txHash, logIndex)`, persist allocation to the invoice atomically, and prevent reuse for another invoice. API `count` is not a substitute for a verified event identity.
5. Keep unavailable, no-indexed-match, candidate and verified-settlement states distinct. No API-only path in this guide returns `paid`.

See [API conventions](README.md) for units and validation, and [wallet integration](wallet-integration.md) for read-only versus transaction boundaries.
