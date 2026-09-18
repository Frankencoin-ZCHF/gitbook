# Savings API

Savings modules let ZCHF holders earn interest on deposited balances. Use this API to show an account's savings, collected interest and recent activity, compare module rates or follow proposed rate changes. Each chain and module has its own records, so an account may have several separate savings balances.

## Endpoints

| GET path | Response |
| --- | --- |
| `/savings/core/info` | `{status, totalBalance, ratioOfSupply, totalInterest}` |
| `/savings/core/ranked` | Account array, up to 1000 accounts ranked by balance |
| `/savings/core/balance/:account` | `chainId -> module address -> account record` |
| `/savings/core/activity/:account` | Up to 1000 recent activity records, not complete account history |
| `/savings/leadrate/info` | `{rate, proposed, open}`, each keyed by chain and module |
| `/savings/leadrate/rates` | Approved-rate records |
| `/savings/leadrate/proposals` | Indexed rate proposals |
| `/savings/referrer/:referrer/mapping` | `{num, accounts, map}`; `map` is chain -> module -> account -> details |
| `/savings/referrer/:referrer/earnings` | `{earnings, chains, total}`; `earnings` is chain -> module -> account -> scaled ZCHF |

## Build a savings view

1. Fetch `GET /savings/core/info` for module rates and aggregate savings totals.
2. Fetch `/savings/core/balance/:account` with the wallet's address. Select the chain and exact module address in both responses, or show each pair as a separate account row.
3. Display the module's annual simple rate, the account's saved balance and its cumulative collected interest. The [display example](#validated-display-and-hypothetical-projection) keeps these units separate.
4. Fetch `/savings/core/activity/:account` for recent deposits, withdrawals and interest collections. Label this as recent activity: the endpoint returns at most 1000 records with no documented exhaustive pagination.
5. Use [wallet contract reads](wallet-integration.md#displaying-savings) to add pending interest, which is not part of the API's cumulative collected-interest field.

An absent module or an empty response is not a confirmed zero on-chain balance. For complete account history, reconcile an independent block-paginated event index.

## Schemas and units

`status` in `/core/info` is a map from chain ID to module address to module record. `totalBalance`, `ratioOfSupply` and `totalInterest` are **root-level fields**, not entries inside `status`.

| Field | Type and unit |
| --- | --- |
| Module `chainId`, `module` | Number and address |
| Module `balance`, `save`, `withdraw`, `interest` | Raw ZCHF decimal integer strings, 18 decimals |
| Module `rate` | Number, annual simple rate in PPM |
| Module `updated` | Unix seconds, number |
| Module/account `counter` | Object of event counts |
| Root `totalBalance`, `totalInterest` | Already scaled ZCHF numbers |
| Root `ratioOfSupply` | Fraction, not percentage |
| Account `account`, `module`, `chainId` | Identity fields, not a top-level account wrapper |
| Account `created`, `updated` | Unix seconds, numbers |
| Activity `kind`, `amount`, `txHash`, `blockheight` | Event kind, raw ZCHF amount, hash and block number |

Account `interest` is cumulative indexed **collected** interest, not a live pending-interest quote. The indexed gross interest total need not equal the net amount credited to the saver after referral fees. Referrer endpoints differ from core endpoints: referral balances and earnings are scaled numbers, and `referrerFee` is PPM. Do not apply the core raw-string conversion to them.

Example `/core/balance/:account` response (historical values):

```json
{
  "1": {
    "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38": {
      "chainId": 1,
      "account": "0x963ec454423cd543db08bc38fc7b3036b425b301",
      "module": "0x27d9ad987bde08a0d083ef7e0e4043c857a17b38",
      "balance": "2000000000000000000000000",
      "created": 1751307767,
      "updated": 1785535811,
      "save": "8285068007024581430745819",
      "interest": "11897690286241121258229",
      "withdraw": "6296965697310822552004048",
      "counter": {"save": 14, "interest": 25, "withdraw": 22}
    }
  }
}
```

## Rates, accrual and module selection

The rate is set through governance proposals and changes, not automatically calculated from reserve metrics. For `rate=40000`, the annual simple fraction is `40000 / 1000000 = 0.04`, or 4%. Select the chain **and exact module address**; do not select the first result of `Object.values` or assume that every module has the same rate.

The contract accrues simple interest using rate ticks. Collecting interest through a state-changing refresh adds net interest to the saved balance, after which that balance can earn interest. APY therefore depends on refresh frequency, changing rates, entry delays, fees and integer rounding. The API's `rate` is not an automatically compounded APY.

For a hypothetical unchanged rate and an already interest-eligible balance, gross interest in base units is `floor(principal * ratePPM * seconds / 1000000 / 31536000)`. This is an estimate, not the live contract calculation across rate changes or delayed entry. Read `accruedInterest` for current gross pending interest on the chosen module. With a nonzero referrer, the inspected referral-capable contract deducts `floor(gross * referralFeePPM / 1000000)`; the remainder is net interest.

Module presence does not identify its ABI or version. Configure those explicitly. The [wallet guide](wallet-integration.md) distinguishes referral-capable modules from older interfaces and explains how to deposit, collect interest and withdraw.

### Follow rate changes

Use `/savings/leadrate/info` to show current approved rates alongside proposed changes. Its `rate`, `proposed` and `open` maps are each keyed by chain and module. Keep a proposal separate from the active rate until the corresponding change takes effect. `/savings/leadrate/rates` and `/savings/leadrate/proposals` provide the indexed records for rate-history and proposal views; `approvedRate` also uses PPM.

### Track referral earnings

Pass the referrer's address to `/savings/referrer/:referrer/mapping` to find referred accounts, grouped by chain, module and account. Join those identities to `/savings/referrer/:referrer/earnings` for an earnings breakdown, or use its `chains` and `total` fields for summaries. Referral balances and earnings are already scaled ZCHF numbers. `referrerFee` is PPM, not a ZCHF amount.

## Validated display and hypothetical projection

Fetch `/savings/core/info` and `/savings/core/balance/:account` with `getJson` from the [shared example](README.md#executable-examples), then pass the parsed responses to `savingsDisplay`. Missing data throws rather than displaying zero. `estimateSimple` uses already eligible seconds and a constant rate; it is not a substitute for the contract's tick calculation.

```javascript
import {object, uint, address, formatUnits} from './README.mjs';

function integer(value, maximum) {
  if (!Number.isSafeInteger(value) || value < 0 || value > maximum) {
    throw new TypeError('Invalid integer parameter');
  }
  return BigInt(value);
}

export function savingsDisplay(info, balances, chainId, moduleAddress, account) {
  object(info); object(balances);
  if (!Number.isSafeInteger(chainId) || chainId <= 0) throw new TypeError('Invalid chain');
  const module = address(moduleAddress), owner = address(account);
  for (const field of ['totalBalance', 'totalInterest', 'ratioOfSupply']) {
    if (typeof info[field] !== 'number' || !Number.isFinite(info[field]) || info[field] < 0) {
      throw new TypeError(`Invalid ${field}`);
    }
  }
  const status = object(object(object(info.status)[String(chainId)])[module]);
  const balance = object(object(balances[String(chainId)])[module]);
  for (const row of [status, balance]) {
    if (row.chainId !== chainId || address(row.module) !== module) throw new TypeError('Module mismatch');
    for (const field of ['balance', 'save', 'withdraw', 'interest']) uint(row[field]);
  }
  if (address(balance.account) !== owner) throw new TypeError('Account mismatch');
  integer(status.rate, 16777215); // uint24 PPM, not a base-unit ZCHF amount.
  return {
    annualSimplePercent: formatUnits(String(status.rate), 4),
    savedZCHF: formatUnits(balance.balance, 18),
    collectedInterestZCHF: formatUnits(balance.interest, 18)
  };
}

export function estimateSimple(principal, ratePPM, eligibleSeconds, referralFeePPM, hasReferrer) {
  const rate = integer(ratePPM, 16777215);
  const seconds = integer(eligibleSeconds, Number.MAX_SAFE_INTEGER);
  const feeRate = integer(referralFeePPM, 250000);
  if (typeof hasReferrer !== 'boolean') throw new TypeError('Expected referrer state');
  const gross = uint(principal) * rate * seconds / 1000000n / 31536000n;
  const fee = hasReferrer ? gross * feeRate / 1000000n : 0n;
  return {gross: gross.toString(), fee: fee.toString(), net: (gross - fee).toString()};
}
```
