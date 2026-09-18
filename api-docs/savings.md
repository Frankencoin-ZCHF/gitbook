# Savings API

Read savings balances, activity and leadrate proposals. API GET requests do not deposit, withdraw or collect interest. See [wallet integration](wallet-integration.md) for the contract methods.

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

The API exposes no tested exhaustive activity pagination recipe. Reconcile an independent block-paginated event index for complete histories. An empty response or absent module is not a confirmed zero on-chain balance.

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

Captured `/core/balance/:account` response from 18 September 2026:

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

The rate is set through governance proposals and changes, not automatically calculated from reserve metrics. For `rate=40000`, the annual simple fraction is `40000 / 1000000 = 0.04`, or 4%. The captured mainnet modules reported `35000` and `10000`: 3.5% and 1%, respectively. Select the chain **and exact module address**; do not select the first result of `Object.values`.

The contract accrues simple interest using rate ticks. Collecting interest through a state-changing refresh adds net interest to the saved balance, after which that balance can earn interest. APY therefore depends on refresh frequency, changing rates, entry delays, fees and integer rounding. The API's `rate` is not an automatically compounded APY.

For a hypothetical unchanged rate and an already interest-eligible balance, gross interest in base units is `floor(principal * ratePPM * seconds / 1000000 / 31536000)`. This is an estimate, not the live contract calculation across rate changes or delayed entry. Read `accruedInterest` for current gross pending interest on the chosen module. With a nonzero referrer, the inspected referral-capable contract deducts `floor(gross * referralFeePPM / 1000000)`; the remainder is net interest.

The captured mainnet API lists modules `0x27d9ad987bde08a0d083ef7e0e4043c857a17b38` and `0x3bf301b0e2003e75a3e86ab82bd1eff6a9dfb2ae`. Module presence does not identify its ABI or version. Configure those explicitly. The [wallet guide](wallet-integration.md) distinguishes referral-capable modules from older interfaces.
