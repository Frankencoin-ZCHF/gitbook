# Positions API

A position is a borrowing contract that holds collateral against minted ZCHF. Use the Positions API to build a borrower's portfolio, find original positions to inspect for cloning and follow changes in debt, collateral and ownership.

## Endpoints

| GET path | Purpose |
| --- | --- |
| `/positions/list` | Position list |
| `/positions/mapping` | Positions keyed by address |
| `/positions/open` | Indexed open positions |
| `/positions/requests` | Indexed position requests |
| `/positions/owners` | `{num, owners, map}` with lowercase owner-address keys and arrays of positions |
| `/positions/mintingupdates/list` | Recent minting updates |
| `/positions/mintingupdates/mapping` | Updates grouped by position |
| `/positions/mintingupdates/position/:version/:address` | Updates for a position version/address |
| `/positions/mintingupdates/owner/:address` | Owner's minting updates |
| `/positions/owner/:address/fees` | Owner fee history |
| `/positions/owner/:address/debt` | Owner debt history |
| `/positions/owner/:address/history` | Position ownership history |
| `/positions/owner/:address/transfers` | Ownership transfers |

## Build an owner's portfolio

1. Fetch `GET /positions/owners`. The response contains `num`, `owners` and `map`.
2. Validate the owner's address and look it up in `map` using its lowercase form. The value is an array of positions. There is no bare `/positions/owner/:address` route.
3. For each position, show collateral balance, minted debt and state flags using the units below. Keep the position address and `version` for subsequent queries.
4. Add price observations for an indicative valuation using the [prices example](prices.md#indicative-position-valuation). It validates the map and separates an empty portfolio from malformed data.

```bash
curl --fail 'https://api.frankencoin.com/positions/owners'
```

## Fields and units

| Fields | Meaning |
| --- | --- |
| `position`, `owner`, `original`, `collateral`, `zchf` | Contract or owner addresses |
| `version`, `isOriginal`, `isClone` | Lending-contract version and position type |
| `denied`, `closed` | Indexed state flags, not a full transaction-eligibility check |
| `minted`, ZCHF limits/capacities | Raw ZCHF integer strings, 18 decimals |
| `collateralBalance`, `minimumCollateral` | Raw collateral integer strings; use `collateralDecimals` |
| `price` | Contract price scaling, not a fiat display quote: raw price times collateral base units divided by `1e18` yields ZCHF base units |
| `annualInterestPPM`, `reserveContribution` | Integer PPM; the latter is a fraction, not an annual rate |
| `created`, `start`, `expiration`, `challengePeriod` | Seconds; `cooldown` may contain a large sentinel rather than a usable calendar date |

For collateral with `d` decimals, the displayed contract price in ZCHF per whole collateral token is `rawPrice * 10^d / 10^36`. Do not divide all balances or all prices by `1e18`. See [prices](prices.md) for separate off-chain CHF/USD valuations.

## State and history

Original positions have a proposal period; clones derive parameters from an existing original position and remain subject to their own conditions. An indexed “open” position may still be unable to mint because of cooldown, expiry, a challenge or another contract constraint. Read the selected version's state before constructing a transaction.

Use `/positions/requests` to monitor proposals and `/positions/open` to narrow a position browser. To find potential originals for cloning, inspect `isOriginal`, the collateral and the original's conditions; the open list alone is not a list of eligible clones.

### Follow a position or owner

Request `/positions/mintingupdates/position/:version/:address` with the position's lending-contract version and address to inspect its recent updates. Use `/positions/mintingupdates/owner/:address` for the owner's recent minting activity. For example:

```bash
curl --fail 'https://api.frankencoin.com/positions/mintingupdates/position/2/0x826C54287c0C1E2A4D0fbF81E2e734c85C48d3f4'
```

The owner `/fees` and `/debt` routes support fee and debt views; `/history` and `/transfers` explain changes in position ownership. Ownership history matters when attributing earlier activity: a position's current owner need not have owned it when a historical event occurred.

Minting updates and owner history queries can return up to 1000 recent records, with no documented exhaustive pagination route. For complete accounting, reconcile a block-paginated contract-event index against chain state and ownership changes.

See [position mechanics](../positions/README.md) and [challenges](challenges.md). V1/V2 refers to lending contracts, not API releases or the FCS wrapper.
