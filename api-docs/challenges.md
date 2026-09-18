# Challenges API

Read indexed challenges and bids. GET requests report activity; they do not challenge a position or place a bid.

## Endpoints and identifiers

| GET path | Purpose |
| --- | --- |
| `/challenges/list` | `{num, list}` of challenges |
| `/challenges/mapping` | Challenges keyed by challenge ID |
| `/challenges/challengers` | Challenges grouped by challenger |
| `/challenges/positions` | Challenges grouped by position |
| `/challenges/prices` | `{num, ids, map}`; active challenge IDs mapped to current prices, not groups of challenges sharing a price |
| `/challenges/bids/list` | Bid list |
| `/challenges/bids/mapping` | `{num, bidIds, map}` keyed by full bid ID |
| `/challenges/bids/bidders` | Bids grouped by bidder |
| `/challenges/bids/challenges` | Bids grouped by challenge |
| `/challenges/bids/positions` | Bids grouped by position |

A challenge ID has the form `<position>-challenge-<number>`. A bid ID adds `-bid-<numberBid>`. These are distinct keys; `/bids/mapping` is not keyed by challenge ID. Consult the selected response wrapper before iterating a map.

## Units and outcome fields

Challenge rows include `version`, `position`, `number`, `start`, `duration`, `size`, `liqPrice`, `filledSize`, `acquiredCollateral`, `status` and `txHash`. Bid rows add `numberBid`, `bidder`, `bidType`, `bid` and `price`. Amounts and timestamps in the captured rows are decimal strings.

`size`, `filledSize` and `acquiredCollateral` use the position's collateral base units. `bid` uses ZCHF base units. `liqPrice` and bid `price` use the contract price scale: multiplying by collateral base units and dividing by `1e18` yields ZCHF base units. Use collateral decimals to display ZCHF per whole token. A large raw price alone says nothing about undercollateralisation.

`status` is an indexer label. Captured `Success` rows include `acquiredCollateral="0"`; the label does not prove liquidation, collateral acquisition or position closure. Interpret `bidType` and quantities together and check the selected contract's events/state for the economic result. The indexer's full status derivation is not established by these examples.

## Challenge and bid mechanics

For MintingHubV2, the first phase allows aversion at the applicable challenge price. In the subsequent Dutch-auction phase, the price falls and a bid executes the corresponding collateral purchase immediately. Collateral is not held for a batch distribution based on bids collected until a fixed end time.

The challenge's `version`, position and minting hub determine the relevant ABI and rules. Do not apply the V2 explanation indiscriminately to V1 records. See [auction mechanics](../positions/auctions.md) and the [inspected MintingHubV2 source](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/v2/MintingHubV2.sol) for version-specific conditions.
