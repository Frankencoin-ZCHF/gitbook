# Prices API

Price endpoints supply display observations with currency and source information. They are not a uniform protocol oracle and do not set a position's challenge price. Legacy FPS price routes remain FPS routes; see [FCS](fcs.md) for the wrapper's reference prices.

## Endpoints

| GET path | Response or purpose |
| --- | --- |
| `/prices/ticker/:ticker` | `{chf, usd}` numbers for a ticker |
| `/prices/list` | Array of token metadata and price observations |
| `/prices/mapping` | Lowercase address -> price observation |
| `/prices/erc20/mint` | ZCHF metadata |
| `/prices/erc20/fps` | Legacy FPS metadata |
| `/prices/erc20/collateral` | Collateral metadata |
| `/prices/owner/:address/valueLocked` | Year-keyed values, raw ZCHF strings in the reviewed schema; not a current position lookup |
| `/prices/marketChart` | Market-data `prices`, `market_caps`, `total_volumes` series |
| `/prices/history/list` | Available collateral histories keyed by address |
| `/prices/history/:address` | Available history for a token |
| `/prices/history/ratio` | `collateralRatioByFreeFloat` and `collateralRatioBySupply` series |

## Currencies, units and freshness

A mapping observation contains `chainId`, `address`, `name`, `symbol`, `decimals`, `price.chf`, `price.usd`, `source` and `timestamp`. Prices are already scaled fiat values per whole token. `timestamp` is Unix **milliseconds**, unlike transfer and savings timestamps. Sources observed in the review include `defillama`, `thegraph`, `custom` and `null`.

A record with a null source, timestamp zero or zero price may represent unavailable data. Reject missing/stale prices for a valuation rather than substitute zero or silently select another currency. Define a freshness threshold for the application. Preserve the quoted currency and source with each displayed value. A ticker alone is not a unique chain/token identity.

Collateral history uses CHF prices and millisecond timestamp keys. The market-chart schema provides series but does not establish their quote currency in the reviewed description; confirm that feed's denomination before labelling a chart. Available histories are not a promise of complete or continuously sampled coverage.

## Aggregate collateral ratios

The ratio route names two denominator concepts: total supply and free float. The reviewed schema does not establish the full numerator or free-float exclusions. Do not infer the calculation solely from the labels. With the same numerator, a smaller free-float denominator yields a larger ratio; it is not inherently a more conservative measure against the same threshold.

These series do not define universal “healthy” bands or a protocol liquidation threshold. State the valuation assumptions and denominator whenever displaying a ratio. The protocol's challenge mechanism is separate from an off-chain portfolio estimate.

## Indicative position valuation

Use `/positions/owners`, not the nonexistent bare owner route. Match lowercase owner keys and collateral addresses, and use each token's decimals. Both sides of a ratio must use the same currency: collateral units times CHF per token divided by ZCHF debt times CHF per ZCHF. An assumption of one CHF per ZCHF is explicit parity valuation, not an observed exchange price.

The example below returns a rational pair of `BigInt` values for an indicative ratio. It keeps raw balances exact and uses the decimal values already returned by the price API; it cannot restore precision the server has discarded. It treats zero debt as a separate state and rejects missing or stale prices. The caller supplies chain ID, valuation time, freshness limit and an explicit CHF-per-ZCHF quote (or parity assumption).
