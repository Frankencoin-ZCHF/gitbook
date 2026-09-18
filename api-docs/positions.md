# Positions API

Read indexed collateralised lending positions and their history. GET requests do not create, clone, adjust or close positions.

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

There is no bare `/positions/owner/:address` lookup in the reviewed API. Use `/positions/owners` and a validated, lowercase address key. The [prices example](prices.md#indicative-position-valuation) does this without treating malformed maps as empty portfolios.

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

Minting updates and owner history queries can return up to 1000 recent records. These are indexed observations, not a promised complete event ledger. No exhaustive pagination recipe is established here. For complete accounting, reconcile a block-paginated contract-event index against chain state and ownership changes.

See [position mechanics](../positions/README.md) and [challenges](challenges.md). V1/V2 refers to lending contracts, not API releases or the FCS wrapper.
