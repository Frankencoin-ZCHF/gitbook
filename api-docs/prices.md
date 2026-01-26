# Prices API

The Prices API provides access to current and historical price data for all collateral assets in the Frankencoin ecosystem, as well as system-wide collateralization ratios. This is essential for monitoring position health, calculating liquidation thresholds, and displaying accurate financial information.

## Overview

The Prices API enables you to:

- Query current prices for all collateral tokens
- Access historical price data for charting and analysis
- Monitor collateralization ratios across the ecosystem
- Track price feeds for specific collateral assets
- Analyze price trends over time

## Key Concepts

### Price Sources

Prices in the Frankencoin ecosystem come from:
- On-chain oracles (Chainlink, Uniswap TWAP, etc.)
- Position-specific price feeds set during creation
- Aggregated market data

All prices are denominated in CHF (Swiss Francs) or ZCHF.

### Collateralization Ratios

Two key ratios track ecosystem health:
- **Ratio by Free Float**: Collateral value / circulating ZCHF supply
- **Ratio by Total Supply**: Collateral value / total ZCHF supply

These ratios indicate how well-backed the ZCHF stablecoin is by collateral.

## Main Endpoints

### Current Prices

- `GET /prices` - Get current prices for all collateral assets

Returns a simple mapping of collateral addresses to current prices.

### Price History

- `GET /prices/history/list` - Complete price history for all collateral types
- `GET /prices/history/:address` - Price history for a specific collateral token

The history endpoint for a specific token returns:
- Token metadata (name, symbol, decimals, address)
- Current price
- Historical prices as a time-series (timestamp → price mapping)

### Collateralization Ratios

- `GET /prices/history/ratio` - Historical collateralization ratio data

Returns:
- Current timestamp
- `collateralRatioByFreeFloat`: Time series of ratios based on circulating supply
- `collateralRatioBySupply`: Time series of ratios based on total supply

## Use Cases

### Position Health Monitoring

Fetch current prices to calculate if positions are adequately collateralized:

```
GET /prices
```

Then compare position collateral value against minted amount.

### Price Charts

Build historical price charts for collateral assets:

```
GET /prices/history/0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599
```

This returns WBTC price history that can be charted over time.

### System Health Dashboard

Monitor ecosystem-wide collateralization:

```
GET /prices/history/ratio
```

Display ratios over time to show protocol health trends.

### Liquidation Alerts

Compare current prices against position liquidation thresholds to alert users of risks:

1. Get current price: `GET /prices`
2. Fetch user's positions: `GET /positions/owner/:address`
3. Calculate collateralization ratios
4. Alert if approaching liquidation levels

### Multi-Asset Analysis

Compare price performance across different collateral types:

```
GET /prices/history/list
```

Analyze which collateral types are most stable or volatile.

## Data Structure

### Current Price Response

Simple object mapping collateral addresses to prices:

```json
{
  "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": "95000.00",
  "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0": "3500.00"
}
```

### Historical Price Response (Specific Token)

```json
{
  "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
  "name": "Wrapped BTC",
  "symbol": "WBTC",
  "decimals": 8,
  "timestamp": 1768964400003,
  "price": {
    "chf": 70374.6
  },
  "history": {
    "1759158000005": 90567.46,
    "1759161600002": 91163.2,
    ...
  }
}
```

### Collateralization Ratio Response

```json
{
  "timestamp": 1768964400003,
  "collateralRatioByFreeFloat": {
    "1759158000005": 3.138139819821414,
    "1759161600002": 3.142567234521876,
    ...
  },
  "collateralRatioBySupply": {
    "1759158000005": 1.688283955398297,
    "1759161600002": 1.689342187654321,
    ...
  }
}
```

## Understanding Collateral Ratios

### Healthy Ranges

- **Above 1.5**: System is overcollateralized, very healthy
- **1.2 - 1.5**: Normal operating range
- **1.0 - 1.2**: Warning zone, increased risk
- **Below 1.0**: Critical, system is undercollateralized

### Free Float vs Total Supply

- **By Free Float**: More conservative, only counts circulating ZCHF
- **By Supply**: Includes all ZCHF, even locked or uncirculated

The free float ratio is typically higher (more conservative) than the total supply ratio.

## Notes

### Timestamps

- Historical data uses Unix millisecond timestamps as keys
- The main `timestamp` field indicates when data was last updated

### Price Precision

- Prices are in CHF with decimal precision
- Historical endpoints may have varying time intervals between data points

### Performance Considerations

- Price history objects can be large (hundreds of data points)
- Consider caching price data with appropriate TTLs (1-5 minutes for current prices, longer for historical)
- For charting, you may want to downsample historical data client-side

### Integration Best Practices

1. **Poll Current Prices**: Update every 1-5 minutes for position monitoring
2. **Cache Historical Data**: Price history changes infrequently, cache for 15-30 minutes
3. **Handle Missing Data**: Not all timestamps will have data, interpolate when necessary for charts
4. **Monitor Ratios**: Set up alerts when collateralization ratios drop below thresholds
5. **Validate Addresses**: Always validate collateral addresses against the Collateral API before using prices

## Example: Building a Position Monitor

```javascript
// 1. Get current prices
const prices = await fetch('https://api.frankencoin.com/prices').then(r => r.json());

// 2. Get user positions
const positions = await fetch(`https://api.frankencoin.com/positions/owner/${address}`).then(r => r.json());

// 3. Calculate health for each position
positions.map.forEach(position => {
  const collateralPrice = prices[position.collateral];
  const collateralValue = position.collateralBalance * collateralPrice;
  const ratio = collateralValue / position.minted;

  if (ratio < 1.2) {
    console.warn(`Position ${position.position} is at risk!`);
  }
});
```
