# Positions API

The Positions API provides comprehensive access to all collateralized lending positions in the Frankencoin ecosystem. Positions represent borrowing contracts where users lock collateral to mint ZCHF stablecoins.

## Overview

A **position** is a smart contract that holds collateral and allows the owner to mint ZCHF against it. The Positions API enables you to:

- Query all positions and their current state
- Filter positions by status (open, closed, pending)
- Track position ownership and transfers
- Monitor minting activity and history
- Analyze owner debt and fee payments over time

## Key Concepts

### Position Types

- **Original Positions**: Newly proposed positions that undergo a voting period before activation
- **Clone Positions**: Fast-tracked positions based on existing approved collateral types
- **Version 1 vs Version 2**: The protocol has evolved, with V2 positions including additional risk parameters

### Position States

- **Open**: Active positions available for minting
- **Closed**: Positions that have been terminated
- **Denied**: Positions rejected during the voting period
- **Pending**: Newly requested positions awaiting approval (typically within 5 days of creation)

### Minting Updates

Every time a position is adjusted (minting, burning, collateral changes, price adjustments), a **minting update** event is recorded. These provide a complete audit trail of position activity.

## Main Endpoints

### Position Queries

- `GET /positions/list` - Retrieve all positions with complete details
- `GET /positions/mapping` - Get positions as an address-keyed object for efficient lookup
- `GET /positions/open` - Filter for only active, open positions
- `GET /positions/requests` - View recently requested positions awaiting approval
- `GET /positions/owners` - Group positions by owner address

### Minting History

- `GET /positions/mintingupdates/list` - Get latest minting update events across all positions
- `GET /positions/mintingupdates/mapping` - Map minting updates by position address
- `GET /positions/mintingupdates/position/:version/:address` - Get history for a specific position
- `GET /positions/mintingupdates/owner/:address` - Get all minting activity for an owner

### Owner Analytics

- `GET /positions/owner/:address/fees` - Track fee payments over time
- `GET /positions/owner/:address/debt` - View historical debt evolution
- `GET /positions/owner/:address/history` - See which positions were owned when
- `GET /positions/owner/:address/transfers` - Monitor position ownership transfers

## Use Cases

### Portfolio Monitoring

Track all positions owned by a specific address to monitor collateralization ratios, debt levels, and fees paid:

```
GET /positions/mintingupdates/owner/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

### Position Discovery

Find positions available for cloning by filtering for open original positions with specific collateral types:

```
GET /positions/open
```

### Risk Analysis

Monitor newly requested positions to assess protocol risk and participate in governance:

```
GET /positions/requests
```

### Historical Analysis

Track how a position has evolved over time by reviewing all minting updates:

```
GET /positions/mintingupdates/position/2/0x826C54287c0C1E2A4D0fbF81E2e734c85C48d3f4
```

## Data Structure

### Position Object

Each position includes:
- **Identification**: position address, version, owner
- **Collateral Details**: collateral token, balance, decimals, name, symbol
- **Minting Parameters**: limits, available capacity, amount minted, interest rate, fees
- **Status Flags**: isOriginal, isClone, denied, closed
- **Timestamps**: creation, start, cooldown, expiration, challenge period

### Minting Update Object

Each update event contains:
- **Position Info**: position address, owner, collateral details
- **Adjustment Data**: size changed, price adjusted, amount minted/burned
- **Fee Information**: fees paid, timeframe, annual interest rate
- **Metadata**: transaction hash, timestamp, version

## Notes

- All amounts are represented as strings in wei (1e18 for 18-decimal tokens)
- Interest rates are in PPM (parts per million): 20000 PPM = 2% annual
- The API returns up to 1000 most recent records for minting updates and historical queries
- Position addresses are unique identifiers and can be used across endpoints
