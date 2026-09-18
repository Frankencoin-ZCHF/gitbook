# Analytics API

Use the Analytics API to explain changes in the shared equity pool, chart its financial history and break down income, costs and collateral exposure. Transaction logs pair recorded financial events with point-in-time metrics; daily logs provide a smaller series for charts.

[FCS](../pool-shares.md) is the canonical governance and share token. These routes describe the shared equity pool and underlying FPS, so FPS prices, supply and per-token earnings retain their FPS units. Use the [FCS controller](fcs.md) for FCS supply, reference prices and redemption discount data.

## Endpoints and limits

| GET path | Response and use |
| --- | --- |
| `/analytics/profitLossLog` | `{num, logs}`; up to 1000 recent profit/loss observations |
| `/analytics/transactionLog/json` | `{num, logs, pageInfo}`; paginated financial events and metrics |
| `/analytics/transactionLog/csvE18` | Transaction-log page as CSV with scaled amounts |
| `/analytics/dailyLog/json` | `{num, logs}` of available daily snapshots, capped at 1000 |
| `/analytics/dailyLog/csvE18` | Daily snapshots as CSV with scaled amounts |
| `/analytics/fps/exposure` | `{general, exposures}`; underlying FPS metrics and collateral exposure |
| `/analytics/fps/earnings` | Scaled earnings and expense categories for underlying FPS |

## Transaction logs

A transaction-log row describes an indexed financial event through its `kind` and `amount`, identifies its chain and transaction, and includes financial totals at that point. A row such as `Equity:Loss` records a loss; `Savings:Withdrawn` identifies a withdrawal. An equity dashboard can show the event alongside the pool's equity, savings balance and FPS price instead of joining it to today's values.

These are API records derived from indexed activity, not raw on-chain event logs. `txHash` links a row to its transaction, but a transaction can contain several events. The response does not establish that every on-chain event has a corresponding row or that the API's history is immutable.

### Query a page

```bash
curl --fail --get 'https://api.frankencoin.com/analytics/transactionLog/json' \
  --data-urlencode 'firstItem=false' \
  --data-urlencode 'limit=50'
```

Read rows from `logs` and pagination metadata from `pageInfo`; `num` counts rows in this response, not the entire history. The default page size is 50. Set `firstItem=false` for newest first, or `firstItem=true` to start with the oldest available records.

To request the next page, keep the same ordering and pass the previous response's full `pageInfo.endCursor` as `after`. Treat the cursor as opaque: URL-encode it, and do not shorten it or replace it with a row's `count`.

```bash
# Set END_CURSOR to the full pageInfo.endCursor from the previous response.
curl --fail --get 'https://api.frankencoin.com/analytics/transactionLog/json' \
  --data-urlencode 'firstItem=false' \
  --data-urlencode 'limit=50' \
  --data-urlencode "after=${END_CURSOR}"
```

Continue while `pageInfo.hasNextPage` is `true`. If a page lacks a next cursor, repeats a cursor or adds no new rows, stop and report an incomplete traversal rather than looping. Deduplicate overlapping rows without assuming that `txHash` alone identifies a row.

## Financial fields

| Transaction-log field | Meaning and unit |
| --- | --- |
| `chainId`, `txHash` | Chain and originating transaction |
| `count` | Indexed record identifier, not an amount or a pagination cursor |
| `timestamp` | Unix seconds |
| `kind`, `amount` | Recorded financial event and its raw amount with 18 decimals; interpret the asset with the event kind |
| `totalInflow`, `totalOutflow` | Running financial inflow and outflow totals, raw ZCHF with 18 decimals |
| `totalEquity`, `totalSavings` | Point-in-time equity and savings totals, raw ZCHF with 18 decimals |
| `fpsTotalSupply` | Underlying FPS supply, raw FPS with 18 decimals |
| `fpsPrice` | ZCHF per FPS, scaled by `1e18` |
| `realizedNetEarnings` | Realised net earnings, raw ZCHF with 18 decimals |
| `earningsPerFPS` | Earnings in ZCHF per FPS, scaled by `1e18` |

Financial quantities in transaction-log JSON are decimal strings. The [shared formatting helper](README.md#shared-validation-and-exact-display-formatting) displays non-negative raw quantities without losing fractional base units. Preserve the sign separately when formatting a signed net-earnings value.

The transaction schema does not include total ZCHF supply, V1/V2 minting totals or interest rates. Use [ecosystem info](ecosystem.md), [positions](positions.md) and [savings](savings.md) for those current data sources. Current values cannot fill gaps in a historical series.

## Daily snapshots

For a chart of equity, inflows, outflows or underlying FPS metrics, fetch `GET /analytics/dailyLog/json`. Each row supplies a `date`, a Unix-second `timestamp` and the available financial totals, not every transaction field. Financial fields use the same raw units as transaction-log JSON. Daily snapshots avoid processing each transaction when the chart needs only daily observations.

Daily routes expose no pagination parameters. The service loads at most 1000 snapshots in ascending timestamp order. Fetch the available series and select the required dates locally; do not rely on a `limit` query to trim it. Preserve missing dates as gaps, not zero balances, and check the last available date before using the series for a current chart.

## Earnings and exposure

Use `GET /analytics/profitLossLog` for recent recorded changes in profit and loss. Rows identify the chain, minter, `created` time in Unix seconds and `kind`, alongside `amount`, cumulative `profits` and `losses`, and `perFPS`. Amounts and totals are raw ZCHF strings with 18 decimals; `perFPS` is ZCHF per FPS scaled by `1e18`.

Use `GET /analytics/fps/earnings` to break down sources such as `minterProposalFees`, `investFees`, `redeemFees` and `positionProposalFees`, alongside costs such as `savingsInterestCosts` and `otherLossClaims`.

Earnings categories are already scaled ZCHF numbers. Do not divide them by `1e18`. The service derives some categories from other totals, so this breakdown is not an itemised receipt ledger. It describes the underlying pool's earnings, not payments to individual FCS holders.

Use `GET /analytics/fps/exposure` to pair general FPS metrics with per-collateral exposures. This supports a collateral-concentration view alongside the [collateral catalogue](ecosystem.md#collateral-catalogue). Monetary values use their named ZCHF units and are already scaled; `mint.interestAverage` and ratios are fractions, while `positions` fields are counts.

## Export completeness

The transaction CSV endpoint exports a page, not the full history: its default is also 50 rows. Apply `firstItem`, `limit` and `after` as for JSON. `pageInfo=true` appends pagination JSON to the CSV response, so a plain CSV parser must not consume that response unchanged. JSON is simpler for cursor-driven ingestion; use CSV for a selected page or assemble an export after collecting the pages.

Reaching `hasNextPage=false` completes the indexer's available traversal, not reconciliation with the chain. For accounting that needs complete history, reconcile records and totals against a separately validated indexer or block-range contract logs, including receipts and chain reorganisations. The profit/loss endpoint's 1000-record limit is separate from transaction-log pagination.
