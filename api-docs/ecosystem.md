# Ecosystem API

The Ecosystem API provides access to core protocol data including information about the Frankencoin (ZCHF) token, Frankencoin Pool Shares (FPS), minter contracts, and approved collateral types. This set of controllers offers a comprehensive view of the protocol's infrastructure.

## Overview

The Ecosystem API is organized into four main controllers:

1. **Frankencoin Controller** - ZCHF token information and multichain data
2. **FPS Controller** - Frankencoin Pool Shares token and reserve data
3. **Minter Controller** - Minting hub contracts and their status
4. **Collateral Controller** - Approved collateral types and their properties

## Frankencoin Controller

Access comprehensive information about the ZCHF stablecoin across all supported blockchains.

### Endpoint

- `GET /ecosystem/frankencoin/info`

### What It Provides

- **ERC20 Details**: Token name, symbol, decimals
- **Multichain Data**: Supply and contract addresses on each blockchain (Ethereum, Optimism, Base, Arbitrum, Polygon, Gnosis, Avalanche, etc.)
- **Token Metrics**: Current USD price, total supply across all chains
- **FPS Information**: FPS price, supply, and market cap
- **TVL**: Total value locked in USD and CHF

### Use Cases

- Monitor ZCHF distribution across blockchains
- Track total protocol TVL
- Display current token price and supply
- Build multichain explorers
- Analyze which chains have the most ZCHF activity

## FPS Controller

Query data about the Frankencoin Pool Shares (FPS) token, which represents ownership in the protocol's equity pool.

### Endpoints

- `GET /ecosystem/fps/info` - Complete FPS token information

### What It Provides

- **Token Information**: Name, symbol, decimals, contract address
- **Supply Metrics**: Total supply, circulating supply
- **Pricing Data**: Current FPS price in ZCHF
- **Reserve Data**: Total equity, minting capacity
- **Multichain Deployment**: FPS distribution across chains
- **Market Data**: Market cap, price history

### Use Cases

- Calculate FPS token valuation
- Monitor reserve equity backing
- Track FPS distribution across chains
- Analyze investment returns for FPS holders
- Build FPS price charts and calculators

## Minter Controller

Access information about minting hub contracts, which are the factories that create and manage positions.

### Endpoints

- `GET /ecosystem/minter/list` - List all minter contracts
- `GET /ecosystem/minter/address/:address` - Get specific minter details

### What It Provides

- **Minter Identification**: Contract address, version (V1, V2)
- **Status**: Active, deprecated, or proposed
- **Capabilities**: What types of positions this minter can create
- **Statistics**: Number of positions created, total minted amount
- **Blockchain Info**: Which chain the minter operates on

### Use Cases

- Identify which minters to use for creating positions
- Track minting activity across different hub versions
- Verify minter contract addresses for integrations
- Analyze adoption of newer minting hub versions
- Monitor protocol upgrades and migrations

## Collateral Controller

Query approved collateral types and their properties.

### Endpoints

- `GET /ecosystem/collateral/list` - List all approved collateral types

### What It Provides

- **Token Details**: Address, name, symbol, decimals
- **Approval Status**: Whether collateral is active, proposed, or denied
- **Risk Parameters**: Typical interest rates, LTV ratios, reserve contributions
- **Usage Statistics**: Number of positions using this collateral, total amount minted
- **Price Data**: Current collateral price feed information

### Use Cases

- Display available collateral options to users
- Validate collateral addresses before position creation
- Show collateral statistics (most popular, highest minted amounts)
- Filter positions by collateral type
- Build collateral comparison tools
- Monitor new collateral proposals

## Integration Examples

### Building a Position Creator UI

1. Fetch approved collateral types: `GET /ecosystem/collateral/list`
2. Get active minters: `GET /ecosystem/minter/list`
3. Display collateral options with current prices from Prices API
4. Use minter address to interact with smart contracts

### Protocol Dashboard

1. Fetch Frankencoin info for total supply and TVL: `GET /ecosystem/frankencoin/info`
2. Get FPS data for equity metrics: `GET /ecosystem/fps/info`
3. Pull analytics for profit/loss: `GET /analytics/profitLossLog`
4. Display collateral breakdown: `GET /ecosystem/collateral/list`

### Multichain Explorer

1. Query Frankencoin info to get all chain deployments
2. For each chain, display supply, contract address, and activity
3. Show total supply sum across all chains
4. Highlight primary vs secondary chains by supply

## Data Structure Notes

### Chain IDs

Common chain IDs in the ecosystem:

- `1` - Ethereum Mainnet
- `10` - Optimism
- `100` - Gnosis Chain
- `137` - Polygon
- `8453` - Base
- `42161` - Arbitrum
- `43114` - Avalanche

### Version Numbers

- **V1**: Original protocol contracts
- **V2**: Current generation with enhanced risk parameters

### Status Values

- **active**: Currently operational and recommended
- **deprecated**: Older version, still functional but not recommended for new positions
- **proposed**: Under governance review
- **denied**: Rejected by governance

## Best Practices

1. **Cache Strategically**: Ecosystem data changes infrequently, cache for 5-10 minutes
2. **Multichain Handling**: Always check chainId to ensure you're using the correct contract
3. **Version Awareness**: Prefer V2 contracts unless specifically working with legacy positions
4. **Status Checks**: Verify active status before allowing users to interact with minters or collateral
