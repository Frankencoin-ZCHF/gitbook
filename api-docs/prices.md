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

### Prices Controller

#### Current Prices

- `GET /prices/ticker/:ticker` - Get price for a specific ticker symbol (e.g., WBTC, WETH, FPS)
- `GET /prices/list` - Get all token prices with metadata
- `GET /prices/mapping` - Get prices as address-keyed mapping for efficient lookup

#### Token Information

- `GET /prices/erc20/mint` - Get Frankencoin (ZCHF) token information
- `GET /prices/erc20/fps` - Get FPS token information
- `GET /prices/erc20/collateral` - Get all collateral token information

#### Owner Analytics

- `GET /prices/owner/:address/valueLocked` - Get historical time series of total value locked by owner

#### Market Data

- `GET /prices/marketChart` - Get Frankencoin market chart data from CoinGecko (prices, market caps, volumes)

### Prices History Controller

#### Price History

- `GET /prices/history/list` - Complete price history for all collateral types with CHF prices
- `GET /prices/history/:address` - Price history for a specific collateral token

The history endpoint for a specific token returns:
- Token metadata (name, symbol, decimals, address)
- Current price in CHF
- Historical prices as a time-series (timestamp → CHF price mapping)

#### Collateralization Ratios

- `GET /prices/history/ratio` - Historical collateralization ratio data

Returns:
- Current timestamp
- `collateralRatioByFreeFloat`: Time series of ratios based on circulating supply
- `collateralRatioBySupply`: Time series of ratios based on total supply

## Use Cases

### Position Health Monitoring

Fetch current prices to calculate if positions are adequately collateralized:

```
GET /prices/list
```

Then compare position collateral value against minted amount.

### Quick Price Lookup by Ticker

Get the price of a specific token by its symbol:

```
GET /prices/ticker/WBTC
```

Returns price in USD and CHF for WBTC.

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

1. Get current prices: `GET /prices/list`
2. Fetch user's positions: `GET /positions/owner/:address`
3. Calculate collateralization ratios
4. Alert if approaching liquidation levels

### Multi-Asset Analysis

Compare price performance across different collateral types:

```
GET /prices/history/list
```

Analyze which collateral types are most stable or volatile.

### Token Metadata Lookup

Get ERC20 information for system tokens:

```
GET /prices/erc20/mint        # ZCHF token info
GET /prices/erc20/fps         # FPS token info
GET /prices/erc20/collateral  # All collateral tokens
```

### Owner Value Tracking

Track historical value locked by a specific owner across all their positions:

```
GET /prices/owner/0x963eC454423CD543dB08bc38fC7B3036B425b301/valueLocked
```

Returns yearly time series of total collateral value.

### Market Data Integration

Fetch CoinGecko market data for Frankencoin:

```
GET /prices/marketChart
```

Returns prices, market caps, and trading volumes over time.

## Data Structure

### Price List Response

Array of price objects with metadata:

```json
[
  {
    "address": "0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2",
    "name": "Frankencoin Pool Share",
    "symbol": "FPS",
    "decimals": 18,
    "timestamp": 1768915146172,
    "price": {
      "usd": 1555.45,
      "chf": 1234.49
    }
  }
]
```

### Price Mapping Response

Object mapping addresses to price data:

```json
{
  "0x1ba26788dfde592fec8bcb0eaff472a42be341b2": {
    "address": "0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2",
    "name": "Frankencoin Pool Share",
    "symbol": "FPS",
    "decimals": 18,
    "timestamp": 1768915146172,
    "price": {
      "usd": 1555.45,
      "chf": 1234.49
    }
  }
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
const pricesData = await fetch('https://api.frankencoin.com/prices/mapping').then(r => r.json());

// 2. Get user positions
const positions = await fetch(`https://api.frankencoin.com/positions/owners`).then(r => r.json());
const userPositions = positions.map[address] || [];

// 3. Calculate health for each position
userPositions.forEach(position => {
  const priceInfo = pricesData[position.collateral.toLowerCase()];
  const collateralPrice = priceInfo.price.usd;
  const collateralValue = (position.collateralBalance / Math.pow(10, position.collateralDecimals)) * collateralPrice;
  const mintedValue = position.minted / 1e18;
  const ratio = collateralValue / mintedValue;

  if (ratio < 1.2) {
    console.warn(`Position ${position.position} is at risk! Ratio: ${ratio.toFixed(2)}`);
  }
});
```
