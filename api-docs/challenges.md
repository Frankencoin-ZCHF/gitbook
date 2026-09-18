# Challenges API

A challenge tests whether a position's stated collateral price is too high. The Challenges API lets an application follow challenges, inspect bids and show available auction prices. Use it for an auction browser or a position's challenge history; the contract mechanics below explain what the records represent.

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

### Build an auction view

1. Fetch `GET /challenges/list` to show challenge records, or use `/challenges/positions` for a position-centred view.
2. Fetch `GET /challenges/prices`. Iterate its `ids` and read the corresponding entries in `map` to show available prices for active challenge IDs. An empty map supplies no current auction prices.
3. Use `/challenges/bids/challenges` to attach bid history to each challenge. Use `/challenges/bids/mapping` only when looking up a full bid ID.
4. Load the position's collateral decimals and lending-contract version before displaying amounts. Before a bid, read current auction state from the matching contract; an indexed price can lag a changing auction.

```bash
curl --fail 'https://api.frankencoin.com/challenges/prices'
```

## Units and outcome fields

Challenge rows include `version`, `position`, `number`, `start`, `duration`, `size`, `liqPrice`, `filledSize`, `acquiredCollateral`, `status` and `txHash`. Bid rows add `numberBid`, `bidder`, `bidType`, `bid` and `price`. Amounts and timestamps are decimal strings; `start` is Unix seconds and `duration` is seconds.

`size`, `filledSize` and `acquiredCollateral` use the position's collateral base units. `bid` uses ZCHF base units. `liqPrice` and bid `price` use the contract price scale: multiplying by collateral base units and dividing by `1e18` yields ZCHF base units. Use collateral decimals to display ZCHF per whole token. A large raw price alone says nothing about undercollateralisation.

`status` is an indexer label, not a summary of the economic outcome. A `Success` record can have zero `acquiredCollateral`. Show `bidType`, `filledSize` and `acquiredCollateral` alongside the label, and use contract events/state to establish whether collateral changed hands or the position closed. Do not count every `Success` row as a liquidation.

## Challenge and bid mechanics

For MintingHubV2, the first phase allows aversion at the applicable challenge price. In the subsequent Dutch-auction phase, the price falls and a bid executes the corresponding collateral purchase immediately. Collateral is not held for a batch distribution based on bids collected until a fixed end time.

The challenge's `version`, position and minting hub determine the relevant ABI and rules. Do not apply the V2 explanation indiscriminately to V1 records. See [auction mechanics](../positions/auctions.md) and the [MintingHubV2 source](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/8b4c4ab67bb361b91d58c474b87f4608fc4c0566/contracts/minting/v2/MintingHubV2.sol) for version-specific conditions.
