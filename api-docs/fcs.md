# FCS API

Frankencoin Share Token (FCS) is the canonical governance and share token. Use this controller to build an FCS overview with supply, reference prices and the current marginal redemption discount. The two endpoints answer different questions: `/fcs/info` describes the share token, while `/fcs/discount` describes the effect of recent redemptions.

Start with the [share guide](../pool-shares.md) for the holder journey, [FCS mechanics](../fcs.md) for contract rules or [migration](../fcs-migration.md) for existing holdings. Underlying FPS supply, prices, reserve data and earnings remain under the FPS routes; they are not FCS metrics.

## GET /fcs/info

Request `GET /fcs/info` for token metadata, its reported chain/address and the `token` metrics. Example response (historical values, not a current quote):

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

Display the price fields as ZCHF per FCS, `totalSupply` as FCS and `totalAssets` as ZCHF. These values are already scaled; dividing them by `1e18` would scale them twice.

FCS wraps legacy FPS one for one, but ZCHF is the ERC-4626 vault asset. Wrapping FPS and depositing ZCHF are different entry paths. FCS supply measures issued wrapper shares; it is not the total supply of underlying FPS.

## GET /fcs/discount

Request `GET /fcs/discount` alongside the overview to show the marginal multiplier and recovery countdown. Example response (historical values):

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

The seven-day recovery applies absent further redemptions; further activity can extend it. A multiplier of `1` means no reduction at the margin. A size-specific redemption can receive a different multiplier, so the countdown and `discount` belong in an overview, not in a calculation of guaranteed proceeds.

The API substitutes `0` if reading `bid()` fails and `1` if reading `currentDiscount(0)` fails. These values do not distinguish a successful read from a failed call. Use a direct contract read when the distinction affects a quote.

## Contract reads and transactions

To connect the overview to a deposit or redemption form:

1. Resolve the selected chain, FCS contract and ABI. Choose the operation: `deposit` and `withdraw` take ZCHF assets; `mint` and `redeem` take FCS shares.
2. Call the corresponding `previewDeposit`, `previewMint`, `previewWithdraw` or `previewRedeem` with the user's amount in base units for a size-specific quote.
3. Read `maxDeposit`, `maxMint`, `maxWithdraw` or `maxRedeem` for the account and check applicable holder/wrapper conditions. Previews calculate amounts; limits and eligibility determine whether the operation is available.
4. Refresh the quote and limits before asking the wallet to submit the transaction. Display the API's reference prices separately from that quote.

`convertToAssets` is a reference conversion, not discounted redemption proceeds. Use each operation's own preview and limit.

For a governance view, read holder votes and eligibility from the contracts rather than inferring them from supply or price. Direct FPS wrapping carries votes; fresh ZCHF entry and WFPS migration do not supply immediate votes. Internal wrapper quorum and the wrapper's legacy FPS quorum are separate.

## Source and version boundary

The contract mechanics above refer to the [ChainSecurity FPS2 report](https://reports.chainsecurity.com/Frankencoin/ChainSecurity_Frankencoin_FPS2_Audit.pdf), final V3 at `c1f229e3b26050367aafcb55da294342b4cae382` (14 July 2026). It calls the wrapper FPS2; it does not establish the identity of a deployed contract. The [FCS service source at `9013d8f`](https://github.com/Frankencoin-ZCHF/frankencoin-api/blob/9013d8fadf2bcc251d236c78328958ebcfbe1c26/src/modules/fcs/fcs.service.ts) defines the field conversions and fallbacks.
