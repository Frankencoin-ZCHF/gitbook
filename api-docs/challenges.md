# Challenges API

The Challenges API provides access to liquidation challenges and auction data within the Frankencoin ecosystem. Challenges are the protocol's mechanism for maintaining system health by allowing anyone to liquidate undercollateralized positions.

## Overview

A **challenge** occurs when someone believes a position is undercollateralized and initiates a liquidation process. The Challenges API enables you to:

- Query all challenges and their outcomes
- Track active and historical auctions
- Monitor bidding activity
- Analyze challenge success rates by position, challenger, or collateral type
- Identify liquidation opportunities

## Key Concepts

### How Challenges Work

1. **Initiation**: Anyone can challenge a position they believe is undercollateralized
2. **Duration**: Challenges run for a fixed period determined by the position's approval method
3. **Bidding**: Other users can bid to take over the collateral by repaying debt
4. **Settlement**: When the challenge period ends, collateral is distributed based on bids received

### Challenge Status

- **Success**: Challenge completed successfully, position was liquidated
- **Failed**: Challenge did not succeed (rare, but possible if position improves)
- **Active**: Challenge currently in progress (bidding open)

## Main Endpoints

### Challenge Queries

- `GET /challenges/list` - Retrieve all challenges with complete details
- `GET /challenges/mapping` - Get challenges as an ID-keyed object
- `GET /challenges/prices` - View challenges grouped by liquidation price
- `GET /challenges/positions` - Group challenges by position address
- `GET /challenges/challengers` - Group challenges by challenger address

### Bid Queries

- `GET /challenges/bids/list` - Get all bids across all challenges
- `GET /challenges/bids/mapping` - Map bids by challenge ID
- `GET /challenges/bids/challenges` - Group bids by challenge
- `GET /challenges/bids/positions` - View bids organized by position
- `GET /challenges/bids/bidders` - Track bidding activity by bidder address

## Use Cases

### Liquidation Monitoring

Track all challenges to understand liquidation events and their outcomes:

```
GET /challenges/list
```

### Challenger Analysis

Identify the most active challengers in the ecosystem:

```
GET /challenges/challengers
```

### Position Risk Assessment

See which positions have been challenged historically to assess risk:

```
GET /challenges/positions
```

### Auction Participation

Monitor active challenges and place bids to acquire collateral at liquidation prices:

```
GET /challenges/bids/list
```

### Market Analysis

Analyze liquidation prices to understand market conditions and collateral value perceptions:

```
GET /challenges/prices
```

## Data Structure

### Challenge Object

Each challenge includes:
- **Identification**: challenge ID, version, challenge number
- **Participants**: position address, challenger address
- **Timing**: start time, creation time, duration
- **Financial Data**: size, liquidation price, filled size, acquired collateral
- **Bidding Info**: number of bids received
- **Outcome**: status (Success, Failed, Active)

### Bid Object

Each bid contains:
- **Challenge Reference**: challenge ID, position, challenger
- **Bidder Info**: bidder address, bid timestamp
- **Bid Details**: bid amount, price, filled amount
- **Collateral**: amount of collateral acquired
- **Metadata**: transaction hash, version

## Notes

- Challenge durations vary based on how the position was approved (common durations are 86400 seconds or 604800 seconds)
- Liquidation prices (`liqPrice`) can be very high, indicating positions that were severely undercollateralized
- The `filledSize` shows how much of the challenge was successfully liquidated through bids
- `acquiredCollateral` represents the total collateral distributed to bidders
- Most challenges result in "Success" status, indicating the liquidation mechanism is working effectively

## Historical Significance

Challenge data provides valuable insights into:
- Protocol health and risk management effectiveness
- Collateral volatility and market stress events
- User participation in liquidation mechanisms
- Position management behavior (frequent challenges may indicate poor risk management)
