# Analytics API

The Analytics API provides comprehensive ecosystem-wide metrics, financial analytics, and historical data for the Frankencoin protocol. This controller aggregates data from across the ecosystem to provide insights into protocol performance, FPS token economics, and system health.

## Overview

The Analytics API enables you to:

- Track profit and loss across the ecosystem
- Monitor transaction logs with full financial context
- Analyze daily aggregated metrics
- Understand FPS token collateral exposure
- Break down FPS earnings sources
- Generate historical reports and charts

## Key Concepts

### Profit & Loss Tracking

The protocol tracks all gains (profits) and losses from various sources:
- **Profits**: Minting fees, position fees, investment fees, trade fees
- **Losses**: Liquidation losses, interest paid on savings, redemption costs

These are tracked cumulatively and per FPS token, providing transparency into protocol economics.

### Transaction Logs

Every significant event affecting the Frankencoin supply, equity, or FPS is logged with complete financial metrics at that moment in time. This creates an immutable audit trail of the protocol's financial state.

### Daily Aggregations

End-of-day snapshots provide clean time-series data for charting trends without processing thousands of individual transactions.

## Main Endpoints

### Profit & Loss

- `GET /analytics/profitLossLog` - Complete log of all profit and loss events (limited to 1000 most recent)

Returns cumulative totals and per-event breakdown of gains and losses.

### Transaction Logs

- `GET /analytics/transactionLog/json` - Paginated transaction history with full metrics
- `GET /analytics/transactionLog/csvE18` - Transaction log formatted as CSV with decimal conversion

Transaction logs include:
- Event type (Mint, Burn, Position creation, etc.)
- Total supply, equity, and savings at that moment
- FPS price and supply
- Interest rates and projected earnings
- Minting totals for V1 and V2 positions

### Daily Aggregations

- `GET /analytics/dailyLog/json` - Daily aggregated metrics in JSON format
- `GET /analytics/dailyLog/csvE18` - Daily metrics as CSV with decimal conversion

Daily logs provide end-of-day snapshots of:
- Supply and equity evolution
- FPS pricing over time
- Cumulative inflows and outflows
- Interest rate trends

### FPS Analytics

- `GET /analytics/fps/exposure` - Detailed collateral exposure analysis for FPS token
- `GET /analytics/fps/earnings` - Complete breakdown of FPS earnings sources

## Use Cases

### Protocol Health Monitoring

Track cumulative profits and losses to ensure protocol sustainability:

```
GET /analytics/profitLossLog
```

### Historical Charts

Generate time-series charts of key metrics using daily aggregated data:

```
GET /analytics/dailyLog/json
```

### FPS Valuation

Understand FPS token value by analyzing collateral backing and earnings:

```
GET /analytics/fps/exposure
GET /analytics/fps/earnings
```

### Financial Reporting

Export complete transaction history in CSV format for external analysis:

```
GET /analytics/transactionLog/csvE18
```

### Risk Assessment

Analyze collateral exposure to understand concentration risk:

```
GET /analytics/fps/exposure
```

## Data Structure

### Profit/Loss Log Entry

- Event details: timestamp, count, event type
- Financial impact: amount gained/lost
- Cumulative totals: running profit and loss totals
- Per-FPS metrics: gains/losses per token

### Transaction Log Entry

- Event identification: timestamp, type, transaction hash
- Supply metrics: total supply, equity, savings
- FPS data: price, supply, market cap
- Minting data: V1 and V2 totals, limits
- Interest rates: current rates, projected earnings
- Borrowing rates: annual rates for V1 and V2

### Daily Log Entry

Similar to transaction logs but aggregated once per day, providing cleaner time-series data.

### FPS Exposure Analysis

- **General Metrics**: FPS price, supply, market cap, earnings, P/E ratio
- **Per-Collateral Exposure**:
  - Collateral details (address, name, symbol)
  - Position counts (open, original, clones)
  - Minting totals and interest averages
  - Risk metrics and loss scenarios

### FPS Earnings Breakdown

Detailed accounting of all revenue sources:
- Minter proposal fees
- Position proposal fees
- Investment and redemption fees
- Other profit claims and contributions
- Savings interest costs (expenses)
- Other loss claims

## Notes

### Data Formats

- **JSON endpoints**: Return structured data for programmatic access
- **CSV endpoints**: Return comma-separated values with all amounts converted from wei to decimal (÷ 1e18)
- Pagination is available on transaction logs using `firstItem`, `limit`, and `after` parameters

### Precision

- All amounts in JSON are in wei (strings)
- CSV exports automatically convert to human-readable decimals
- Interest rates are in wei representation (divide by 1e18 for percentage)

### Performance

- Daily logs are more efficient than transaction logs for charting
- Transaction logs support pagination for managing large datasets
- Profit/loss logs and FPS analytics are limited to relevant recent data

## Example Workflow

### Building a Dashboard

1. Fetch daily logs for historical charts
2. Get FPS exposure for current risk assessment
3. Pull profit/loss log for income statement
4. Use FPS earnings for detailed revenue breakdown

This provides a complete picture of protocol performance and health.
