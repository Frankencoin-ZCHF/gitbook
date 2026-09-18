# Prices API

Use the Prices API to display token prices, chart collateral price history and estimate the fiat value of a position. Each observation carries currency and source information so that an application can keep a valuation tied to its inputs.

These display prices are not a uniform protocol oracle and do not set a position's challenge price. For the canonical share token's reference prices, use [FCS](fcs.md). FPS price routes here report the underlying FPS token, not an FCS market price.

## Endpoints

| GET path | Response or purpose |
| --- | --- |
| `/prices/ticker/:ticker` | `{chf, usd}` numbers for a ticker |
| `/prices/list` | Array of token metadata and price observations |
| `/prices/mapping` | Lowercase address -> price observation |
| `/prices/erc20/mint` | ZCHF metadata |
| `/prices/erc20/fps` | Legacy FPS metadata |
| `/prices/erc20/collateral` | Collateral metadata |
| `/prices/owner/:address/valueLocked` | Year-keyed values in raw ZCHF strings; use the Positions API for current positions |
| `/prices/marketChart` | Market-data `prices`, `market_caps`, `total_volumes` series |
| `/prices/history/list` | Available collateral histories keyed by address |
| `/prices/history/:address` | Available history for a token |
| `/prices/history/ratio` | `collateralRatioByFreeFloat` and `collateralRatioBySupply` series |

## Currencies, units and freshness

A mapping observation contains `chainId`, `address`, `name`, `symbol`, `decimals`, `price.chf`, `price.usd`, `source` and `timestamp`. Prices are already scaled fiat values per whole token. `timestamp` is Unix **milliseconds**, unlike transfer and savings timestamps. Sources include `defillama`, `thegraph`, `custom` and `null`.

A record with a null source, timestamp zero or zero price may represent unavailable data. Reject missing/stale prices for a valuation rather than substitute zero or silently select another currency. Define a freshness threshold for the application. Preserve the quoted currency and source with each displayed value. A ticker alone is not a unique chain/token identity.

### Look up a price and build a chart

For a quick ticker display, request `/prices/ticker/:ticker`, for example:

```bash
curl --fail 'https://api.frankencoin.com/prices/ticker/WBTC'
```

Read `chf` or `usd` according to the display currency. For portfolio work, fetch `/prices/mapping` instead, select the lowercase collateral address and verify the observation's chain ID and decimals against the position.

To chart one collateral, request `/prices/history/:address`. Read its CHF prices, convert millisecond timestamp keys to dates and sort the observations chronologically. Use `/prices/history/list` when the view needs several collateral histories. Keep gaps visible; observations need not arrive at regular intervals.

The separate `/prices/marketChart` route provides `prices`, `market_caps` and `total_volumes` series. Its schema does not specify the quote currency, so confirm the feed's denomination before labelling the chart.

## Aggregate collateral ratios

Use `/prices/history/ratio` to plot the `collateralRatioBySupply` and `collateralRatioByFreeFloat` series separately. The names distinguish total supply from free float, but the schema does not specify the full numerator or free-float exclusions. Confirm those inputs before comparing the series to an external ratio. With the same numerator, a smaller free-float denominator yields a larger ratio; it is not inherently a more conservative measure against the same threshold.

These series do not define universal “healthy” bands or a protocol liquidation threshold. State the valuation assumptions and denominator whenever displaying a ratio. The protocol's challenge mechanism is separate from an off-chain portfolio estimate.

## Indicative position valuation

Fetch the owner's positions from `/positions/owners` and price observations from `/prices/mapping`. Match lowercase owner keys and collateral addresses, and use each token's decimals. Both sides of a ratio must use the same currency: collateral units times CHF per token divided by ZCHF debt times CHF per ZCHF. An assumption of one CHF per ZCHF is explicit parity valuation, not an observed exchange price.

The example below returns a rational pair of `BigInt` values for an indicative ratio. It keeps raw balances exact and uses the decimal values already returned by the price API; it cannot restore precision the server has discarded. It treats zero debt as a separate state and rejects missing or stale prices. The caller supplies chain ID, the ZCHF contract address, valuation time, freshness limit and an explicit CHF-per-ZCHF quote (or parity assumption).

```javascript
import {object, uint, address, formatUnits} from './README.mjs';

export function ownerPositions(response, owner) {
  const map = object(object(response).map, 'owner map');
  const rows = map[address(owner)];
  if (rows === undefined) return [];
  if (!Array.isArray(rows)) throw new TypeError('Expected position array');
  for (const row of rows) {
    if (address(object(row).owner) !== address(owner)) throw new TypeError('Owner mismatch');
  }
  return rows;
}

function decimal(value) {
  if (typeof value !== 'number' && typeof value !== 'string') throw new TypeError('Invalid decimal');
  if (typeof value === 'number' && (!Number.isFinite(value) || value <= 0)) throw new TypeError('Invalid quote');
  const match = /^(0|[1-9][0-9]*)(?:\.([0-9]+))?(?:e([+-]?[0-9]+))?$/i.exec(String(value));
  if (!match) throw new TypeError('Invalid decimal quote');
  const fraction = match[2] || '';
  const scale = fraction.length - Number(match[3] || 0);
  if (!Number.isSafeInteger(scale) || Math.abs(scale) > 255) throw new RangeError('Quote scale');
  let numerator = BigInt(match[1] + fraction), denominator = 1n;
  if (numerator === 0n) throw new RangeError('Quote must be positive');
  if (scale >= 0) denominator = 10n ** BigInt(scale);
  else numerator *= 10n ** BigInt(-scale);
  return {numerator, denominator};
}

export function indicativeRatio(position, observation, config) {
  object(position); object(config);
  if (!Number.isSafeInteger(config.chainId) || config.chainId <= 0 ||
      address(position.zchf) !== address(config.zchfAddress)) throw new TypeError('Asset mismatch');
  const collateral = uint(position.collateralBalance), debt = uint(position.minted);
  const decimals = position.collateralDecimals;
  if (!Number.isInteger(decimals) || decimals < 0 || decimals > 255) throw new TypeError('Invalid decimals');
  const zchf = decimal(config.zchfChf);
  if (debt === 0n) return {status: 'no-debt'};
  object(observation, 'price observation');
  if (observation.chainId !== config.chainId ||
      address(observation.address) !== address(position.collateral) ||
      observation.decimals !== decimals) throw new TypeError('Collateral identity mismatch');
  const {nowMs, maxAgeMs} = config;
  if (!Number.isSafeInteger(nowMs) || !Number.isSafeInteger(maxAgeMs) || maxAgeMs < 0 ||
      !Number.isSafeInteger(observation.timestamp) || observation.timestamp <= 0 ||
      observation.timestamp > nowMs || nowMs - observation.timestamp > maxAgeMs ||
      typeof observation.source !== 'string' || observation.source.length === 0) {
    throw new Error('Missing or stale price');
  }
  const chf = decimal(object(observation.price).chf);
  const numerator = collateral * chf.numerator * zchf.denominator * 10n ** 18n;
  const denominator = 10n ** BigInt(decimals) * chf.denominator * debt * zchf.numerator;
  return {status: 'indicative', currency: 'CHF', numerator: numerator.toString(),
    denominator: denominator.toString(), ratioDecimal: formatUnits((numerator * 1000000n / denominator).toString(), 6)};
}
```

`ratioDecimal` truncates to six decimal places for display. The numerator and denominator preserve the exact ratio of the supplied decimal inputs. The caller can fetch both maps with the [shared GET helper](README.md#executable-examples), then use `priceMap[position.collateral.toLowerCase()]`. An unsupported chain or missing observation is an error, not a zero valuation.
