# Savings API

The Savings API provides access to the Frankencoin savings module, which allows users to deposit ZCHF and earn interest. The API is organized into three controllers that handle core savings functionality, lead rate calculations, and referrer rewards.

## Overview

The Savings module enables ZCHF holders to earn yield by depositing into savings contracts. The API provides:

- Current savings balances and interest rates across all chains
- Historical interest rate changes and proposals
- Lead rate calculations (the competitive interest rate)
- Referrer information and reward tracking

## Deployed Contracts

Savings modules are deployed across multiple blockchains. The API aggregates data from all chains.

| Chain | Address | Explorer |
|-------|---------|----------|
| Ethereum | `0x27d9AD987BdE08a0d083ef7e0e4043C857A17B38` | [Etherscan](https://etherscan.io/address/0x27d9ad987bde08a0d083ef7e0e4043c857a17b38) |
| Polygon | `0xb519bae359727e69990c27241bef29b394a0acbd` | [Polygonscan](https://polygonscan.com/address/0xb519bae359727e69990c27241bef29b394a0acbd) |
| Gnosis | `0xbf594d0fed79ae56d910cb01b5dd4f4c57b04402` | [Gnosisscan](https://gnosisscan.io/address/0xbf594d0fed79ae56d910cb01b5dd4f4c57b04402) |
| Arbitrum | `0xb41715e54e9f0827821a149ae8ec1af70aa70180` | [Arbiscan](https://arbiscan.io/address/0xb41715e54e9f0827821a149ae8ec1af70aa70180) |
| Optimism | `0x6426324af1b14df3cd03b2d500529083c5ea61bc` | [Optimistic Etherscan](https://optimistic.etherscan.io/address/0x6426324af1b14df3cd03b2d500529083c5ea61bc) |
| Base | `0x6426324af1b14df3cd03b2d500529083c5ea61bc` | [Basescan](https://basescan.org/address/0x6426324af1b14df3cd03b2d500529083c5ea61bc) |
| Avalanche | `0x8e7c2a697751a1ce7a8db51f01b883a27c5c8325` | [Snowtrace](https://snowtrace.io/address/0x8e7c2a697751a1ce7a8db51f01b883a27c5c8325) |

## Smart Contract Interaction

In addition to the data API described below, you can interact directly with the savings smart contract on-chain. The source code is available on [GitHub](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/savings/Savings.sol).

### Reading Balances

Each account's saved balance is stored in the `savings` mapping:

```solidity
mapping(address => Account) public savings;
```

To get the current saved balance (excluding accrued but uncollected interest), read `savings[owner].saved`.

To get the accrued interest that has not yet been collected, call the view function:

```solidity
function accruedInterest(address accountOwner) public view returns (uint192)
```

The total balance of a user is `savings[owner].saved + accruedInterest(owner)`.

### Adding Savings

To deposit ZCHF into the savings module, call one of the `save` functions. The caller must have approved the savings contract to spend ZCHF on their behalf.

```solidity
// Save to your own account
function save(uint192 amount) public

// Save to another account
function save(address owner, uint192 amount) public
```

Alternatively, use `adjust` to set the balance to a target amount. This will deposit or withdraw as needed:

```solidity
function adjust(uint192 targetAmount) public
```

Note that newly deposited funds are subject to a 3-day delay before interest starts accruing.

### Withdrawing Savings

To withdraw ZCHF from the savings module:

```solidity
function withdraw(address target, uint192 amount) public returns (uint256)
```

If the requested amount exceeds the available balance, the entire balance is withdrawn. The function returns the actual amount transferred.

### Refreshing Balances

Interest does not compound automatically. Anyone can trigger an accumulation of accrued interest (together with a payout of any referrer fee) by calling:

```solidity
// Refresh another account's balance
function refreshBalance(address owner) public returns (uint192)

// Shortcut for refreshBalance(msg.sender)
function refreshMyBalance() public returns (uint192)
```

Calling `refreshBalance` collects the accrued interest and adds it to the account balance. It can be beneficial to do so periodically in order to start earning interest on the previously accrued interest. This can be called by anyone — not just the account owner — making it useful for keeper bots or referrers who want to trigger their fee payout.

### Referrer and Referral Fee

Frontends and wallets can earn a share of the interest collected by their users by setting a referrer. The referral fee is capped at **25% (250,000 ppm)** and is deducted from the collected interest.

To save and set a referrer in a single transaction:

```solidity
function save(uint192 amount, address referrer, uint24 referralFeePPM) public
```

The referrer can also be set when adjusting or withdrawing:

```solidity
function adjust(uint192 targetAmount, address referrer, uint24 referralFeePPM) public
function withdraw(uint192 amount, address referrer, uint24 referralFeePPM) public
```

A user can remove their referrer at any time:

```solidity
function dropReferrer() public
```

The referral fee is paid out automatically whenever interest is collected (e.g., via `refreshBalance`). The user can change or drop their referrer at any time, so the fee is not sticky — it depends on the convenience the frontend provides.

## Key Concepts

### How Savings Works

1. Users deposit ZCHF into savings modules on any supported chain
2. Interest accrues based on the current savings rate (with a 3-day initial delay)
3. Rates are adjusted through governance proposals
4. Users can withdraw their balance plus earned interest at any time

### Interest Rate System

- **Savings Rate**: The APY paid to depositors
- **Lead Rate**: A calculated competitive rate based on various protocol metrics
- **Rate Proposals**: Changes to the savings rate must go through a governance process

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
