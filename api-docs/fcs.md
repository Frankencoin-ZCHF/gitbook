# FCS API

The Frankencoin Share Token (FCS) has its own controller. Legacy FPS supply, prices, reserve data and earnings remain under the FPS routes; they are not FCS metrics. See [FCS mechanics](../fcs.md) and [migration](../fcs-migration.md) for the token and voting model.

## GET /fcs/info

Captured response from 18 September 2026, not a current quote:

```json
{
  "erc20": {"name": "Frankencoin Share", "symbol": "FCS", "decimals": 18},
  "chain": {"chainId": 1, "address": "0xDb861830D9Ae2d1fCF99fA0cfd3973de382B0B5b"},
  "token": {
    "ask": 1282.183703648763,
    "bid": 1282.183703648763,
    "totalAssets": 94965.24027041676,
    "totalSupply": 222.19571189409976,
    "isBinding": false
  }
}
```

| Field | Type and meaning |
| --- | --- |
| `erc20` | Reported name, symbol and decimals |
| `chain` | One chain/address object, not the FPS `chains` map |
| `token.ask`, `token.bid` | Scaled numbers in ZCHF per FCS, from contract reference prices; not secondary-market quotes or size-specific execution previews |
| `token.totalAssets` | Scaled ZCHF value; in audited V3, `ZCHF.equity() * totalSupply() / FPS1.totalSupply()`, the wrapper holders' fraction of equity |
| `token.totalSupply` | Scaled FCS supply, not total legacy FPS supply |
| `token.isBinding` | Boolean returned by the wrapper; binding depends on its share of underlying FPS voting power, not FCS token supply |

FCS wraps legacy FPS one for one, but ZCHF is the ERC-4626 vault asset. Wrapping FPS and depositing ZCHF are different entry paths. The same captured API reported legacy FPS at `0x1bA26788dfDe592fec8bcB0Eaff472a42BE341B2`, with a supply of `8566.157674440636`. Equal ask/bid values do not make the two supplies interchangeable.

## GET /fcs/discount

Captured response from the same review:

```json
{
  "discount": 1,
  "recentlyRedeemed": "0",
  "weightedRecentRedemptions": "0",
  "redemptionAnchor": 0,
  "recoveryPeriodSeconds": 604800,
  "recoveryCountdownSeconds": 0
}
```

| Field | Type and meaning |
| --- | --- |
| `discount` | Scaled marginal multiplier from `currentDiscount(0)`; `1` means no reduction, not a 1% discount |
| `recentlyRedeemed` | Raw FCS quantity as a decimal integer string (18 decimals) |
| `weightedRecentRedemptions` | Time-decayed redemption quantity as a decimal integer string (18 decimals) |
| `redemptionAnchor` | Unix seconds, number |
| `recoveryPeriodSeconds` | Recovery period in seconds |
| `recoveryCountdownSeconds` | Number, `max(0, anchor + period - API server time)` |

The seven-day recovery applies absent further redemptions; further activity can extend it. This marginal multiplier is not the discount for every redemption size. The inspected API source substitutes `0` if reading `bid()` fails and `1` if reading `currentDiscount(0)` fails. These fallbacks do not distinguish a successful read from a failed call.

## Contract reads and transactions

For a size-specific quote, use the selected deployment's `previewDeposit`, `previewMint`, `previewWithdraw` or `previewRedeem`. Read the corresponding `maxDeposit`, `maxMint`, `maxWithdraw` or `maxRedeem` and applicable holder/wrapper conditions. Previews calculate amounts; limits and eligibility determine whether the operation is available. `convertToAssets` is a reference conversion, not discounted redemption proceeds. `withdraw` takes assets; `redeem` takes shares, and their limits differ.

This controller neither reports per-holder voting eligibility nor submits transactions. Direct FPS wrapping carries votes; fresh ZCHF entry and WFPS migration do not supply immediate votes. Internal wrapper quorum and the wrapper's legacy FPS quorum are separate. These conditions belong to contract state, not a price field.

## Source and version boundary

The [ChainSecurity FPS2 report](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf), final V3 at `c1f229e3b26050367aafcb55da294342b4cae382` (14 July 2026), is the source for the versioned contract mechanics above. It calls the wrapper FPS2. Deployment fields are captured API responses. Field conversions and fallback behaviour come from [FCS service source at `9013d8f`](https://github.com/Frankencoin-ZCHF/frankencoin-api/blob/9013d8fadf2bcc251d236c78328958ebcfbe1c26/src/modules/fcs/fcs.service.ts).
