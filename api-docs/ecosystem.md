# Ecosystem API

These GET endpoints report indexed token information, minter proposals and collateral used in positions. See [API conventions](README.md) for units and [FCS](fcs.md) for the separate wrapper controller.

## Frankencoin and legacy FPS

| GET path | Response |
| --- | --- |
| `/ecosystem/frankencoin/info` | `erc20`, `chains`, `token`, `fps`, `tvl` objects |
| `/ecosystem/frankencoin/keyvalues` | Metric-ID map of `{id, value, amount}`; interpret `amount` by metric, since it can be a count or a raw quantity |
| `/ecosystem/frankencoin/totalsupply` | ZCHF supply summary, not FCS supply |
| `/ecosystem/coinmarketcap/totalsupply` | Supply route for the market-data integration |
| `/ecosystem/fps/info` | Legacy FPS `erc20`, `chains`, `token`, `earnings`, `reserve` objects |

Frankencoin info has `token.usd` (USD per ZCHF), `token.supply` (scaled ZCHF), chain-specific `supply` values, and `tvl.usd`/`tvl.chf`. The embedded `fps` object remains legacy FPS.

FPS info has `token.price` (ZCHF per FPS), `token.totalSupply` (FPS), `token.marketCap` (ZCHF), `earnings.profit`/`loss` and `reserve.balance`/`equity`/`minter` (ZCHF). These are already scaled JSON numbers. It does not supply `circulatingSupply`, `priceHistory` or `mintingCapacity`. Use the [prices history routes](prices.md) for available historical observations; minting eligibility requires the relevant contract state.

## Minter proposals

- `GET /ecosystem/minter/list`
- `GET /ecosystem/minter/list/:chainId`

The response is `{num, list}`. A proposal contains `chainId`, `minter`, `suggestor`, `txHash`, `applicationPeriod`, `applicationFee`, `applyMessage` and `applyDate`, plus nullable denial fields `denyMessage`, `denyDate`, `denyTxHash` and `vetor` (the API's spelling).

Dates and application periods are seconds; `applicationFee` is a raw ZCHF string. The list includes denied proposals. It has no `active/deprecated/proposed` enum or version field. A null denial field does not establish current authorisation. For contract interaction, resolve the selected chain and minter address, proposal/denial timing and current authorisation on chain.

## Collateral catalogue

| GET path | Purpose |
| --- | --- |
| `/ecosystem/collateral/list` | `{num, list}` of token metadata |
| `/ecosystem/collateral/mapping` | Address-keyed metadata |
| `/ecosystem/collateral/positions` | Positions grouped by collateral |
| `/ecosystem/collateral/positions/details` | Grouped position details |
| `/ecosystem/collateral/stats` | Collateral statistics |

Metadata includes `chainId`, `address`, `name`, `symbol` and `decimals`. Catalogue membership records use in indexed positions, not approval of a new position or a collateral whitelist. Original positions and clones have their own conditions.

Position V1/V2 identifies a lending-contract version. It does not identify the FCS governance migration, API version or savings module version. Resolve chain, address and ABI from the [contract repository](https://github.com/Frankencoin-ZCHF/FrankenCoin) and [published SDK](https://www.npmjs.com/package/@frankencoin/zchf), pinned to the deployment used by the application.
