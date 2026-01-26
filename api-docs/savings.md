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

- `GET /savings/core/info` - Complete savings module information across all chains
- `GET /savings/core/list` - List all savings events (deposits, withdrawals, interest payments)
- `GET /savings/core/account/:address` - Get savings data for a specific account

### What It Provides

**Per-Chain Data**:
- Module contract address
- Total balance in savings
- Accrued interest
- Total deposits and withdrawals
- Current interest rate
- Event counters (interest payments, rate changes, rate proposals)

**Aggregate Metrics**:
- Total balance across all chains
- Percentage of total ZCHF supply in savings
- Total interest earned system-wide

**Account-Specific Data**:
- User's balance on each chain
- Interest earned by the user
- Deposit and withdrawal history

### Use Cases

#### Savings Dashboard

Display total savings TVL and interest rates:

```
GET /savings/core/info
```

#### User Portfolio

Show a user's savings balance and earned interest:

```
GET /savings/core/account/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

#### Yield Comparison

Compare savings rates across different chains (though typically they're uniform):

```
GET /savings/core/info
```

Filter the response by chain ID to compare rates.

## Leadrate Controller

Access lead rate calculations, which represent the competitive interest rate the protocol should offer.

### Endpoints

- `GET /savings/leadrate/current` - Get current lead rate calculation
- `GET /savings/leadrate/history` - Historical lead rate data

### What It Provides

- Calculated lead rate based on protocol metrics
- Components used in the lead rate formula
- Historical evolution of the lead rate
- Comparison between lead rate and actual savings rate

### Use Cases

#### Rate Policy Monitoring

Compare the current savings rate to the calculated lead rate:

```
GET /savings/leadrate/current
GET /savings/core/info
```

If the actual rate differs significantly from the lead rate, it may indicate a need for rate adjustment.

#### Rate Trend Analysis

Track how the competitive rate has evolved:

```
GET /savings/leadrate/history
```

Chart this data to show rate trends over time.

## Referrer Controller

Access referrer program data for tracking who refers new savers and their rewards.

### Endpoints

- `GET /savings/referrer/list` - List all referrers and their referral counts
- `GET /savings/referrer/address/:address` - Get referrer statistics for a specific address
- `GET /savings/referrer/referred/:address` - See who referred a specific address

### What It Provides

- Referrer addresses and their referral counts
- Rewards earned by referrers
- Referral relationships (who referred whom)
- Referrer performance metrics

### Use Cases

#### Referral Program Dashboard

Display top referrers and their statistics:

```
GET /savings/referrer/list
```

#### Referrer Rewards Tracking

Show rewards earned by a specific referrer:

```
GET /savings/referrer/address/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

#### Referral Verification

Check if a user was referred and by whom:

```
GET /savings/referrer/referred/0x6a4a629d14EC0fc8e2b7DB41949FefaA4F63327F
```

## Data Structure

### Savings Info Response

```json
{
  "status": {
    "1": {  // Ethereum
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
    "totalBalance": 5000000.00,
    "ratioOfSupply": 0.25,
    "totalInterest": 250000.00
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

Interest rates in the API are typically expressed in wei (1e18 precision):
- `500000000000000000` = 0.5 = 50% APY
- `30000000000000000` = 0.03 = 3% APY

To convert to percentage: `(rate / 1e18) * 100`

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
const savingsInfo = await fetch('https://api.frankencoin.com/savings/core/info')
  .then(r => r.json());

// Get rate from Ethereum mainnet
const ethModule = Object.values(savingsInfo.status[1])[0];
const rate = ethModule.rate / 1e18; // Convert to decimal

// Calculate estimated earnings
const principal = 10000; // ZCHF
const timeYears = 1;
const interest = principal * rate * timeYears;
console.log(`Estimated interest: ${interest} ZCHF`);
```

### Savings Tracker

```javascript
// Get user's current savings
const account = await fetch(`https://api.frankencoin.com/savings/core/account/${userAddress}`)
  .then(r => r.json());

// Display across all chains
Object.entries(account.chains).forEach(([chainId, data]) => {
  console.log(`Chain ${chainId}: ${data.balance / 1e18} ZCHF`);
  console.log(`Interest earned: ${data.interest / 1e18} ZCHF`);
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
