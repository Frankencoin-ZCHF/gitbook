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
| `from`, `sender`, `to` | Addresses; `from` and original `sender` can differ. Validate before case-normalised comparison |
| `reference` | Exact public reference string, possibly empty |
| `targetChain` | Decimal string: `0` is the same-chain sentinel; otherwise a CCIP chain selector, **not** an EIP-155 ID |
| `txHash` | Full source-chain transaction hash |

Keep CCIP selectors as strings or `BigInt`; some exceed JavaScript's safe integer range. Resolve nonzero selectors against the maintained CCIP configuration for the relevant deployment. Never compare `chainId !== targetChain` to detect destination settlement. A source-chain reference event does not establish receipt on the destination chain.

## Invoice integration boundary

A reference/amount match is only a **candidate for verification**. This API record does not supply the token-emitting address, log index, receipt success, confirmations, or destination settlement proof needed to authorise delivery.

Before crediting a payment:

1. Require the intended recipient, payer policy, exact invoice identifier, chain, token contract and integer amount. Reject underpayment; handle partial/overpayments under an explicit business policy.
2. Fetch and validate the successful transaction receipt on the expected chain. Decode the correct contract's reference and token events and bind them to each other; matching a hash alone is insufficient.
3. Apply a chain-specific finality/reorg policy. For bridges, verify destination token, recipient and settlement independently.
4. Deduplicate by `(chainId, txHash, logIndex)`, persist allocation to the invoice atomically, and prevent reuse for another invoice. API `count` is not a substitute for a verified event identity.
5. Keep unavailable, no-indexed-match, candidate and verified-settlement states distinct. No API-only path in this guide returns `paid`.

## Candidate lookup example

This example accepts only same-chain candidates and never reports `paid`. It matches one transfer against the full invoice amount; it does not aggregate partial payments. Duplicate API rows are collapsed for display only. Receipt-level event deduplication and invoice allocation remain separate.

```javascript
import {object, uint, address, getJson} from './README.mjs';

function invoiceFields(invoice) {
  object(invoice);
  const from = address(invoice.from), to = address(invoice.to);
  if (!Number.isSafeInteger(invoice.chainId) || invoice.chainId <= 0 ||
      typeof invoice.reference !== 'string' || invoice.reference.length === 0 ||
      uint(invoice.amount) === 0n) throw new TypeError('Invalid invoice requirements');
  return {...invoice, from, to};
}

export function matchCandidates(rows, invoice) {
  const expected = invoiceFields(invoice);
  if (!Array.isArray(rows)) throw new TypeError('Expected transfer array');
  const candidates = new Map();
  for (const row of rows) {
    object(row, 'transfer');
    const from = address(row.from), to = address(row.to);
    address(row.sender);
    const amount = uint(row.amount);
    uint(row.targetChain);
    for (const field of ['count', 'created']) {
      if (typeof row[field] === 'number') {
        if (!Number.isSafeInteger(row[field]) || row[field] < 0) throw new TypeError(field);
      } else uint(row[field]);
    }
    if (!Number.isSafeInteger(row.chainId) || row.chainId <= 0 ||
        typeof row.reference !== 'string' || typeof row.txHash !== 'string' ||
        !/^0x[0-9a-fA-F]{64}$/.test(row.txHash)) throw new TypeError('Invalid transfer');
    if (from === expected.from && to === expected.to && row.chainId === expected.chainId &&
        row.targetChain === '0' && row.reference === expected.reference &&
        amount >= uint(expected.amount)) {
      // Candidate display key only: the API does not expose a receipt logIndex.
      const key = JSON.stringify([row.chainId, row.txHash.toLowerCase(), String(row.count),
        from, to, row.amount, row.reference]);
      candidates.set(key, row);
    }
  }
  return {status: candidates.size ? 'unverified-candidates' : 'no-indexed-match',
    complete: false, candidates: [...candidates.values()]};
}

export async function historyCandidates(invoice, start, end, fetchImpl = fetch) {
  const expected = invoiceFields(invoice);
  const dates = [start, end].map(value => {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.000Z$/.test(value)) {
      throw new TypeError('Use whole-second UTC ISO timestamps');
    }
    const date = new Date(value);
    if (!Number.isFinite(date.getTime()) || date.toISOString() !== value) throw new TypeError('Invalid date');
    return date;
  });
  if (dates[0] >= dates[1]) throw new RangeError('start must precede end');
  const query = new URLSearchParams({to: expected.to, reference: expected.reference, start, end});
  const rows = await getJson(`/transfer/reference/history/by/from/${expected.from}?${query}`, fetchImpl);
  return matchCandidates(rows, expected);
}
```

See [API conventions](README.md) for units and validation, and [wallet integration](wallet-integration.md) for read-only versus transaction boundaries.
