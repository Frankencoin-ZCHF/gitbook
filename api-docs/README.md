# API documentation

Base URL: `https://api.frankencoin.com`. The [interactive specification](https://api.frankencoin.com/) lists routes and parameters. These pages describe read-only HTTP GET requests. They do not create positions, place bids, deposit savings or transfer tokens; those actions use the relevant contracts.

[FCS](../pool-shares.md) is Frankencoin's canonical governance and share token. Start with the [FCS controller](fcs.md) for its supply, reference prices and discount data. FPS routes remain the source for the underlying equity token's data; their identifiers and units do not change with FCS's reader-facing role.

## Controllers

- [FCS](fcs.md): canonical share-token information and redemption discount.
- [Ecosystem](ecosystem.md): ZCHF, underlying FPS, minter proposals and collateral catalogues.
- [Positions](positions.md): indexed lending positions and owner histories.
- [Challenges](challenges.md): indexed challenges, bids and current challenge prices.
- [Prices](prices.md): display prices, currencies, sources and indicative valuations.
- [Savings](savings.md): balances, rates, activity and referrals.
- [Transfers](transfers.md): reference-bearing transfers and candidate matching.
- [Analytics](analytics.md): underlying FPS metrics and shared equity financial logs.
- [Wallet integration](wallet-integration.md): module selection and contract read/write boundaries.

## Versions and data conventions

The response examples and limitations below were checked on 18 September 2026 against API version `0.4.2`, saved public responses and the linked source. API releases, position V1/V2, savings module versions and the FCS audit revision are separate version systems. A cached API result can lag chain state; `/status` reports service/indexer health, not finality for each record.

| Field family | Encoding and unit |
| --- | --- |
| ZCHF/FPS/FCS raw contract amounts | Decimal integer strings, 18 decimals |
| Position collateral balances | Decimal integer strings, use `collateralDecimals`, which may be 0, 6, 8 or 18 |
| Savings module balances and collected interest | Raw ZCHF strings; savings aggregate totals are already scaled JSON numbers |
| Savings `rate`, leadrate `approvedRate` | Integer parts per million (PPM); divide by `1e6` for a fraction or `1e4` for a percentage |
| Ecosystem totals, FPS earnings/exposure, FCS info | Already scaled JSON numbers for display; do not divide again |
| Transfer `created`, savings `updated`, analytics `timestamp` | Unix seconds; some endpoints encode these as decimal strings |
| Prices mapping `timestamp` | Unix milliseconds; `0` can mean no usable price |
| Status `lastChecked` | ISO timestamp string |
| `targetChain` | Decimal CCIP selector string, not an EIP-155 chain ID |

There is no global “all amounts are wei” or “all timestamps are seconds” rule. Keep raw quantities as integer strings/`BigInt`. JSON numbers may already have lost precision; do not use display totals to construct transaction amounts. Validate field types and units for each endpoint. Missing, null or malformed data is distinct from zero.

## Executable examples

The JavaScript blocks are ES modules for Node.js 18+ or a compatible browser. Save each page's JavaScript block as its page name plus `.mjs`, keeping them in one directory (`README.mjs`, `transfers.mjs`, `savings.mjs`, `prices.mjs`). Imports below refer to those files. Functions only perform GET requests when called; tests use recorded responses or explicitly labelled synthetic fixtures.

From a repository checkout, run `python3 scripts/check-api-docs.py`. It extracts these exact blocks, checks JSON examples and local links, and runs the offline tests without installing dependencies.

### Shared validation and exact display formatting

`getJson` rejects HTTP errors, error envelopes and malformed JSON. This helper accepts object/array endpoints; scalar endpoints need a separate validator. Endpoint functions must also check the expected schema. It propagates failures rather than treating them as empty results. `formatUnits` retains fractional base units without converting to `Number`.

```javascript
export function object(value, label = 'object') {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new TypeError(`Expected ${label}`);
  }
  return value;
}

export function uint(value) {
  if (typeof value !== 'string' || !/^(0|[1-9][0-9]*)$/.test(value)) {
    throw new TypeError('Expected a decimal unsigned integer string');
  }
  return BigInt(value);
}

export function address(value) {
  if (typeof value !== 'string' || !/^0x[0-9a-fA-F]{40}$/.test(value)) {
    throw new TypeError('Expected a 20-byte address');
  }
  return value.toLowerCase();
}

export function formatUnits(raw, decimals) {
  const amount = uint(raw);
  if (!Number.isInteger(decimals) || decimals < 0 || decimals > 255) {
    throw new TypeError('Invalid decimals');
  }
  if (decimals === 0) return amount.toString();
  const digits = amount.toString().padStart(decimals + 1, '0');
  const fraction = digits.slice(-decimals).replace(/0+$/, '');
  return digits.slice(0, -decimals) + (fraction ? `.${fraction}` : '');
}

export async function getJson(path, fetchImpl = fetch) {
  if (typeof path !== 'string' || !path.startsWith('/') || path.startsWith('//')) {
    throw new TypeError('Expected an API-relative path');
  }
  const url = new URL(path, 'https://api.frankencoin.com');
  if (url.origin !== 'https://api.frankencoin.com') throw new TypeError('Invalid origin');
  const response = await fetchImpl(url, {
    method: 'GET', redirect: 'error', signal: AbortSignal.timeout(10000)
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
  if (data === null || typeof data !== 'object' ||
      'error' in data || 'errors' in data || 'statusCode' in data) {
    throw new Error('Invalid API response or error envelope');
  }
  return data;
}
```

The address helper validates syntax, not EIP-55 checksum or contract identity. Use a chain-aware address registry and the selected contract's ABI when moving from indexed data to contract calls.
