# Savings API

The Savings API provides access to the Frankencoin savings module, which allows users to deposit ZCHF and earn interest. The API is organized into three controllers that handle core savings functionality, lead rate calculations, and referrer rewards.

## Overview

The Savings module enables ZCHF holders to earn yield by depositing into savings contracts. The API provides:

- Current savings balances and interest rates across all chains
- Historical interest rate changes and proposals
- Lead rate calculations (the competitive interest rate)
- Referrer information and reward tracking

## Key Concepts

### How Savings Works

1. Users deposit ZCHF into savings modules on any supported chain
2. Interest accrues based on the current savings rate
3. Rates are adjusted through governance proposals
4. Users can withdraw their balance plus earned interest at any time

### Interest Rate System

- **Savings Rate**: The APY paid to depositors
- **Lead Rate**: A calculated competitive rate based on various protocol metrics
- **Rate Proposals**: Changes to the savings rate must go through a governance process

### Multichain Savings

Savings modules are deployed across multiple blockchains, and the API aggregates data from all chains.

## Savings Core Controller

Access core savings module data including balances, rates, and transaction history.

### Endpoints

- `GET /savings/core/info` - Complete savings ecosystem information across all chains and modules
- `GET /savings/core/ranked` - Get ranked savings accounts by balance (top 1000)
- `GET /savings/core/balance/:account` - Get savings balance for a specific account
- `GET /savings/core/activity/:account` - Get savings activity history for a specific account

### What It Provides

#### `/info` endpoint:

**Per-Chain and Module Status**:

- Module contract addresses
- Total balance in each module
- Accrued interest
- Total saved and withdrawn amounts
- Current interest rate (in PPM)
- Event counters (interest collections, rate changes, rate proposals, save/withdraw transactions)

**Aggregate Metrics**:

- Total balance across all modules
- Ratio of ZCHF total supply in savings
- Total interest collected system-wide

#### `/ranked` endpoint:

- Latest 1000 savings accounts sorted by balance
- Balance, save/interest/withdraw totals per account
- Transaction counters per account
- Chain and module information

#### `/balance/:account` endpoint:

- Account balance organized by chain ID and module address
- Created and updated timestamps
- Save, interest, and withdraw totals
- Transaction counters

#### `/activity/:account` endpoint:

- Recent activity history (Saved, Withdrawn, InterestCollected, RateChanged events)
- Amounts, balances, timestamps
- Transaction hashes and block heights
- Current rates at time of activity

### Use Cases

#### Savings Dashboard

Display total savings TVL and interest rates:

```
GET /savings/core/info
```

#### User Portfolio

Show a user's savings balance and earned interest:

```
GET /savings/core/balance/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

#### Activity Tracking

View complete transaction history for an account:

```
GET /savings/core/activity/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

#### Leaderboard

Display top savers in the ecosystem:

```
GET /savings/core/ranked
```

## Leadrate Controller

Access lead rate information, proposals, and approved rates across all chains and savings modules.

### Endpoints

- `GET /savings/leadrate/info` - Complete lead rate information including current rates, proposals, and open proposals
- `GET /savings/leadrate/rates` - Currently approved lead rates per chain and module
- `GET /savings/leadrate/proposals` - All lead rate proposals and their history

### What It Provides

#### `/info` endpoint:

**Current Approved Rates** per chain and module:

- Approved interest rate in PPM
- Approval timestamp and transaction hash
- Rate change counter

**Proposed Rate Changes** per chain and module:

- Proposer address
- Next rate to be applied
- Timestamp when rate will change
- Proposal transaction details

**Open Proposals**:

- Pending rate proposals awaiting execution
- Comparison between current and next rates
- Sync status across chains

#### `/rates` endpoint:

- Latest approved rate per module
- Complete historical list of all rate changes
- Rate progression over time

#### `/proposals` endpoint:

- Latest proposal per module
- Complete historical list of all proposals
- Proposer information and timing

### Use Cases

#### Rate Policy Monitoring

View current rates and pending proposals:

```
GET /savings/leadrate/info
```

Track when rate changes will take effect.

#### Rate History Analysis

Review how interest rates have evolved:

```
GET /savings/leadrate/rates
```

Analyze rate adjustment patterns.

#### Governance Participation

Monitor rate proposals to participate in governance:

```
GET /savings/leadrate/proposals
```

View who proposed changes and when they'll be executed.

## Referrer Controller

Access referrer program data for tracking savings accounts that use referrers and their earnings.

### Endpoints

- `GET /savings/referrer/:referrer/mapping` - Get all savings accounts using a specific referrer
- `GET /savings/referrer/:referrer/earnings` - Get total earnings for a specific referrer

### What It Provides

#### `/:referrer/mapping` endpoint:

**Account Mapping** organized by chain ID, module, and account address:

- Account creation and update timestamps
- Current savings balance
- Referrer address and fee percentage (in PPM)
- Total number of accounts using this referrer
- Array of all account addresses

#### `/:referrer/earnings` endpoint:

**Earnings Breakdown**:

- Nested mapping of earnings: chain → module → account → amount
- Total earnings per chain
- Overall total earnings across all chains

### Use Cases

#### Referral Program Dashboard

View all accounts referred by a specific address:

```
GET /savings/referrer/0x0000000000000000000000000000000000000000/mapping
```

For default referrer (zero address), shows unreferred accounts.

#### Referrer Rewards Tracking

Calculate total earnings for a referrer:

```
GET /savings/referrer/0x963eC454423CD543dB08bc38fC7B3036B425b301/earnings
```

Shows breakdown of earnings per account and chain.

#### Referral Performance Analysis

Combine both endpoints to analyze referrer performance:

```
GET /savings/referrer/:address/mapping  # Get account count
GET /savings/referrer/:address/earnings # Get total rewards
```

## Data Structure

### Savings Info Response

```json
{
	"status": {
		"1": {
			// Ethereum
			"0xmodule_address": {
				"chainId": 1,
				"updated": 1768964400,
				"module": "0x...",
				"balance": "1000000000000000000000000",
				"interest": "50000000000000000000000",
				"save": "1200000000000000000000000",
				"withdraw": "200000000000000000000000",
				"rate": "500000000000000000",
				"counter": {
					"interest": 100,
					"rateChanged": 5,
					"rateProposed": 8,
					"save": 1500,
					"withdraw": 300
				}
			}
		},
		// ... other chains
		"totalBalance": 5000000.0,
		"ratioOfSupply": 0.25,
		"totalInterest": 250000.0
	}
}
```

### Account Response

```json
{
	"address": "0x963eC454423CD543dB08bc38fC7B3036B425b301",
	"chains": {
		"1": {
			"balance": "1000000000000000000000",
			"interest": "50000000000000000000"
		}
	},
	"totalBalance": "1000000000000000000000",
	"totalInterest": "50000000000000000000"
}
```

## Understanding Interest Rates

### Rate Format

Interest rates in the API are expressed in PPM (parts per million):

- `40000` = 4% APY (40000 / 1000000 = 0.04)
- `15000` = 1.5% APY (15000 / 1000000 = 0.015)

To convert to percentage: `(rate / 1000000) * 100`

Referrer fees are also in PPM.

### Rate Calculation

The lead rate is calculated using:

- Borrowing costs from positions
- FPS token earnings
- Protocol revenue
- Market conditions

## Integration Examples

### Savings Calculator

```javascript
// Fetch current rate
const savingsInfo = await fetch(
	'https://api.frankencoin.com/savings/core/info',
).then((r) => r.json());

// Get rate from Ethereum mainnet module
const ethModule = Object.values(savingsInfo.status['1'])[0];
const rate = ethModule.rate / 1000000; // Convert from PPM to decimal

// Calculate estimated earnings
const principal = 10000; // ZCHF
const timeYears = 1;
const interest = principal * rate * timeYears;
console.log(`Estimated interest: ${interest.toFixed(2)} ZCHF`);
console.log(`Current APY: ${(rate * 100).toFixed(2)}%`);
```

### Savings Tracker

```javascript
// Get user's current savings
const account = await fetch(
	`https://api.frankencoin.com/savings/core/balance/${userAddress}`,
).then((r) => r.json());

// Display across all chains and modules
Object.entries(account).forEach(([chainId, modules]) => {
	Object.entries(modules).forEach(([moduleAddress, data]) => {
		console.log(`Chain ${chainId}, Module ${moduleAddress}:`);
		console.log(
			`  Balance: ${(BigInt(data.balance) / BigInt(1e18)).toString()} ZCHF`,
		);
		console.log(
			`  Interest earned: ${(BigInt(data.interest) / BigInt(1e18)).toString()} ZCHF`,
		);
	});
});
```

## Notes

### Multichain Considerations

- Savings modules are independent per chain
- Interest rates are typically the same across all chains but can vary
- Users must deposit on each chain separately

### Rate Updates

- Interest rates can change through governance
- Check `rateProposed` vs `rateChanged` counters to see pending changes
- Historical rate data helps predict future rate trends

### Performance

- Savings info is relatively static, cache for 5-10 minutes
- Account data should be fetched more frequently (1-2 minutes) for real-time balance updates
- Referrer data changes infrequently, cache for 10-15 minutes

### Best Practices

1. **Display APY Clearly**: Always convert rates from wei to human-readable percentages
2. **Show All Chains**: Users may have savings on multiple chains
3. **Calculate Returns**: Provide calculators to show estimated earnings
4. **Historical Context**: Show rate history so users understand rate stability
5. **Referral Attribution**: If implementing referrals, always track and display referrer info
