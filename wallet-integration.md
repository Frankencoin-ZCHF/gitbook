---
description: Developer guide for integrating Frankencoin and the Savings Module into wallets and applications
---

# 🪪 Wallet Integration

This guide provides developers with the technical details needed to integrate Frankencoin (ZCHF) and its native savings module into wallets, applications, and services.

## Frankencoin Token (ZCHF)

### ERC-20 Standard

Frankencoin is a standard ERC-20 token that implements all standard functions:

-   `balanceOf(address account)`
-   `totalSupply()`
-   `transfer(address to, uint256 amount)`
-   `transferFrom(address from, address to, uint256 amount)`
-   `allowance(address owner, address spender)`
-   `approve(address spender, uint256 amount)`

### Multi-chain Support

Frankencoin is deployed across multiple blockchain networks, allowing users to interact with ZCHF on their preferred chain. When integrating, ensure your wallet supports the relevant chain IDs.

### Interface Reference

The complete ERC-20 interface can be found in the official repository:
[IERC20.sol](https://github.com/Frankencoin-ZCHF/Frankencoin/blob/main/contracts/erc20/IERC20.sol)

## Savings Module Integration

The Frankencoin savings module allows users to lock up Frankencoins to earn yield. This feature can be integrated natively into wallets to provide users with seamless access to earning opportunities.

### Core Concepts

The savings module uses an `Account` structure that tracks:

-   `saved`: Amount of ZCHF currently saved
-   `ticks`: Internal counter for interest calculation
-   `referrer`: Optional address for referral fees
-   `referralFeePPM`: Referral fee in parts per million (ppm)

### Events

The savings module emits three primary events:

```solidity
event Saved(address indexed account, uint192 amount);
event InterestCollected(address indexed account, uint256 interest, uint256 referrerFee);
event Withdrawn(address indexed account, uint192 amount);
```

### Key Constants

```solidity
uint64 public immutable INTEREST_DELAY = uint64(3 days);
```

Interest accrues after a 3-day delay from when funds are saved.

### Data Structure

```solidity
mapping(address => Account) public savings;

struct Account {
    uint192 saved;
    uint64 ticks;
    address referrer;
    uint32 referralFeePPM;
}
```

### Core Functions

#### Query Functions

```solidity
// Refresh and return the current balance for an account
function refreshBalance(address owner) public returns (uint192)

// View accrued interest for an account at current time
function accruedInterest(address accountOwner) public view returns (uint192)

// View accrued interest for an account at a specific timestamp
function accruedInterest(address accountOwner, uint256 timestamp) public view returns (uint192)
```

#### Basic Operations

```solidity
// Save ZCHF from caller's wallet
function save(uint192 amount) public

// Save ZCHF on behalf of another address
function save(address owner, uint192 amount) public

// Withdraw ZCHF to a target address
function withdraw(address target, uint192 amount) public returns (uint256)

// Adjust savings to a target amount (save or withdraw as needed)
function adjust(uint192 targetAmount) public
```

#### Referral Functions

The savings module includes a referral system that allows wallets and frontends to earn fees by facilitating user interactions:

```solidity
// Save with referrer
function save(uint192 amount, address referrer, uint24 referralFeePPM) public

// Withdraw with referrer
function withdraw(uint192 amount, address referrer, uint24 referralFeePPM) public

// Adjust with referrer
function adjust(uint192 targetAmount, address referrer, uint24 referralFeePPM) public

// Drop the current referrer
function dropReferrer() public
```

### Referral Logic

The referral system allows wallets and frontends to monetize their integration:

-   Referral fees can be up to **25%** (250,000 ppm) of earned interest
-   Fees are deducted from the collected interest, not the principal
-   Users can drop or change referrers at any time
-   The fee represents convenience value - users pay for easier interaction with the protocol

**Important**: The referral fee is not sticky. Users retain full control and can modify or remove referrers, so the fee depends on the convenience and value your wallet provides.

## API Helper Endpoints

Frankencoin provides REST API endpoints to simplify integration without requiring direct blockchain queries.

### Base URL

```
https://api.frankencoin.com
```

### 1. Module Info

Get comprehensive information about all savings modules across all chains.

**Endpoint**: `GET https://api.frankencoin.com/savings/core/info`

**Example Response**:

```json
{
	"status": {
		"1": {
			"0x27d9ad987bde08a0d083ef7e0e4043c857a17b38": {
				"chainId": 1,
				"updated": 1768146791,
				"module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
				"balance": "3252713131296817909181865",
				"interest": "17606356382481561618851",
				"save": "9066019386383589628122254",
				"withdraw": "5830912611469253280559240",
				"rate": 40000,
				"counter": {
					"interest": 350,
					"rateChanged": 2,
					"rateProposed": 1,
					"save": 436,
					"withdraw": 177
				}
			}
		},
		"10": {
			"0x6426324af1b14df3cd03b2d500529083c5ea61bc": {
				"chainId": 10,
				"updated": 1765391881,
				"module": "0x6426324af1b14df3cd03b2d500529083c5ea61bc",
				"balance": "0",
				"interest": "0",
				"save": "0",
				"withdraw": "0",
				"rate": 40000,
				"counter": {
					"interest": 0,
					"rateChanged": 3,
					"rateProposed": 0,
					"save": 0,
					"withdraw": 0
				}
			}
		}
	}
}
```

**Note**: The `rate` is expressed in basis points (e.g., 40000 = 4% annual rate).

**TypeScript Interface**:

```typescript
export type ApiSavingsInfo = {
	status: SavingsStatusMapping;
	totalBalance: number;
	ratioOfSupply: number;
	totalInterest: number;
};

export type SavingsStatusMapping = {
	[K in ChainId]: {
		[module: Address]: SavingsStatus;
	};
};

export type SavingsStatus = {
	chainId: ChainId;
	updated: number;
	module: Address;
	balance: string;
	interest: string;
	save: string;
	withdraw: string;
	rate: number;
	counter: {
		interest: number;
		rateChanged: number;
		rateProposed: number;
		save: number;
		withdraw: number;
	};
};
```

### 2. Ranked Accounts

Get a ranked list of accounts by savings balance across all chains.

**Endpoint**: `GET https://api.frankencoin.com/savings/core/ranked`

**Example Response**:

```json
[
	{
		"chainId": 1,
		"account": "0x963ec454423cd543db08bc38fc7b3036b425b301",
		"module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
		"balance": "800000000000000000000000",
		"created": 1751307767,
		"updated": 1767025931,
		"save": "2999417071917808219178083",
		"interest": "4424985059912480974118",
		"withdraw": "2203842056977720700152201",
		"counter": {
			"save": 4,
			"interest": 9,
			"withdraw": 9
		}
	}
]
```

**TypeScript Interface**:

```typescript
export type ApiSavingsRanked = SavingsBalance[];

export type SavingsBalance = {
	chainId: ChainId;
	account: Address;
	module: Address;
	balance: string;
	created: number;
	updated: number;
	interest: string;
	save: string;
	withdraw: string;
	counter: {
		save: number;
		interest: number;
		withdraw: number;
	};
};
```

### 3. Account Balance

Get savings information for a specific account across all chains and modules.

**Endpoint**: `GET https://api.frankencoin.com/savings/core/balance/<account>`

**Example**: `GET https://api.frankencoin.com/savings/core/balance/0x963ec454423cd543db08bc38fc7b3036b425b301`

**Example Response**:

```json
{
	"1": {
		"0x27d9ad987bde08a0d083ef7e0e4043c857a17b38": {
			"chainId": 1,
			"account": "0x963ec454423cd543db08bc38fc7b3036b425b301",
			"module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
			"balance": "800000000000000000000000",
			"created": 1751307767,
			"updated": 1767025931,
			"save": "2999417071917808219178083",
			"interest": "4424985059912480974118",
			"withdraw": "2203842056977720700152201",
			"counter": {
				"save": 4,
				"interest": 9,
				"withdraw": 9
			}
		}
	}
}
```

**TypeScript Interface**:

```typescript
export type ApiSavingsBalance = {
	[K in ChainId]: {
		[module: Address]: SavingsBalance;
	};
};
```

### 4. Account Activities

Get the latest transaction history for an account's savings activities (limited to 1000 entries).

**Endpoint**: `GET https://api.frankencoin.com/savings/core/activity/<account>`

**Example**: `GET https://api.frankencoin.com/savings/core/activity/0x963ec454423cd543db08bc38fc7b3036b425b301`

**Example Response**:

```json
[
	{
		"chainId": 1,
		"account": "0x963ec454423cd543db08bc38fc7b3036b425b301",
		"module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
		"created": 1767025931,
		"blockheight": 24119513,
		"count": 22,
		"balance": "800000000000000000000000",
		"save": "2999417071917808219178083",
		"interest": "4424985059912480974118",
		"withdraw": "2203842056977720700152201",
		"kind": "Withdrawn",
		"amount": "101791599315068493150684",
		"rate": 40000,
		"txHash": "0xe0d225c67bdc434da108bf359a40d5a6586b03d93a1843897810aa75cf9ae313"
	},
	{
		"chainId": 1,
		"account": "0x963ec454423cd543db08bc38fc7b3036b425b301",
		"module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
		"created": 1767025931,
		"blockheight": 24119513,
		"count": 21,
		"balance": "901791599315068493150684",
		"save": "2999417071917808219178083",
		"interest": "4424985059912480974118",
		"withdraw": "2102050457662652207001517",
		"kind": "InterestCollected",
		"amount": "1791599315068493150684",
		"rate": 40000,
		"txHash": "0xe0d225c67bdc434da108bf359a40d5a6586b03d93a1843897810aa75cf9ae313"
	}
]
```

**Activity kinds**: `Saved`, `Withdrawn`, `InterestCollected`

**TypeScript Interface**:

```typescript
export type ApiSavingsActivity = SavingsActivityQuery[];

export type SavingsActivityQuery = {
	chainId: ChainId;
	account: Address;
	module: Address;
	created: number;
	blockheight: number;
	count: number;
	balance: string;
	save: string;
	interest: string;
	withdraw: string;
	kind: string;
	amount: string;
	rate: number;
	txHash: string;
};
```

### 5. Referrer Mapping

Get detailed information about all accounts that have set a specific address as their referrer.

**Endpoint**: `GET https://api.frankencoin.com/savings/referrer/<refferer>/mapping`

**Example**: `GET https://api.frankencoin.com/savings/referrer/0x963ec454423cd543db08bc38fc7b3036b425b301/mapping`

**Example Response**:

```Json
{
  "num": 1,
  "accounts": ["0x637f00cab9665cb07d91bfb9c6f3fa8fabfef8bc"],
  "map": {
    "1": {
      "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38": {
        "0x637f00cab9665cb07d91bfb9c6f3fa8fabfef8bc": {
          "created": 1751307767,
          "updated": 1767025931,
          "balance": 250000000000000000000000,
          "referrer": "0x963ec454423cd543db08bc38fc7b3036b425b301",
          "referrerFee": 100000
        }
      }
    }
  }
}
```

**TypeScript Interface**:

```typescript
export type ApiSavingsReferrerMapping = {
	num: number;
	accounts: Address[];
	map: SavingsReferrerMapping;
};

export type SavingsReferrerMapping = {
	[K in ChainId]: {
		[module: Address]: {
			[account: Address]: SavingsReferrerAccountItem;
		};
	};
};

export type SavingsReferrerAccountItem = {
	created: number;
	updated: number;
	balance: number;
	referrer: Address;
	referrerFee: number;
};
```

**Use Case**: Referrers can use this endpoint to monitor their referred accounts. They can also trigger the `refreshBalance()` function for these accounts to collect accrued interest and receive their referral fee split.

### 6. Referrer Earnings

Get aggregated earnings information for a referrer across all chains and modules.

**Endpoint**: `GET https://api.frankencoin.com/savings/referrer/<referrer>/earnings`

**Example**: `GET https://api.frankencoin.com/savings/referrer/0x5f238e89F3ba043CF202E1831446cA8C5cd40846/earnings`

**Example Response**:

```Json
{
  "earnings": {
    "1": {
      "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38": {
        "0x637f00cab9665cb07d91bfb9c6f3fa8fabfef8bc": 32.78471424721345
      }
    }
  },
  "chains": {
    "1": 32.78471424721345
  },
  "total": 32.78471424721345
}
```

**TypeScript Interface**:

```typescript
export type ApiSavingsReferrerEarnings = {
	earnings: SavingsReferrerEarnings;
	chains: {
		[K in ChainId]: number;
	};
	total: number;
};

export type SavingsReferrerEarnings = {
	[K in ChainId]: {
		[module: Address]: {
			[account: Address]: number;
		};
	};
};
```

**Use Case**: This endpoint provides referrers with a complete view of their earnings across all chains, making it easy to display total revenue from the referral program.

## NPM Package

For faster integration, use the official Frankencoin API package:

```bash
npm install @frankencoin/api
# or
yarn add @frankencoin/api
```

**Package**: [@frankencoin/api](https://www.npmjs.com/package/@frankencoin/api)

This package provides typed API clients and utilities for interacting with the Frankencoin API endpoints, including all the savings module endpoints described above. All TypeScript types are included, making integration type-safe and easier.

## Integration Best Practices

### For Wallet Developers

1. **Display Savings Balance**: Show users their total ZCHF savings balance alongside their regular ZCHF balance
2. **Accrued Interest**: Use the `accruedInterest()` function to display pending interest in real-time
3. **Simple UX**: Provide one-click "Save" and "Withdraw" buttons with amount inputs
4. **Interest Collection**: Remind users that interest accrues after a 3-day delay
5. **Referral Integration**: Set your wallet address as the referrer to earn a portion of user interest

### For Frontend Developers

1. **Use API Endpoints**: Leverage the REST API for faster queries instead of direct contract calls
2. **Multi-chain Support**: Display savings across all supported chains in a unified interface
3. **Activity History**: Show users their complete savings history using the activity endpoint
4. **Rate Display**: Convert the rate from basis points to a user-friendly percentage (e.g., 40000 → "4% APY")

### Referral Program Recommendations

-   Set a reasonable referral fee (typically 5-15%) to balance user value and wallet revenue
-   Clearly communicate to users that they pay a small convenience fee
-   Allow power users to easily drop the referrer if they prefer direct interaction
-   Use the referrer mapping endpoint to trigger `refreshBalance()` for your referred accounts periodically

## Smart Contract Addresses

For the latest contract addresses across all supported chains, please refer to the [official Frankencoin documentation](https://docs.frankencoin.com) or the [GitHub repository](https://github.com/Frankencoin-ZCHF/Frankencoin).

## Support and Resources

-   [Frankencoin GitHub](https://github.com/Frankencoin-ZCHF/Frankencoin)
-   [Telegram Community](https://t.me/frankencoinzchf)
-   [API Documentation](https://api.frankencoin.com/)
