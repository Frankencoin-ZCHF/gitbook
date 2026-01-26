# Transfers API

The Transfers API provides access to ZCHF transfer data with custom reference messages. This enables users to attach metadata to their transfers, such as invoice numbers, payment purposes, or notes, creating an on-chain payment reference system.

## Overview

The Transfer Reference system allows ZCHF transfers to include custom string messages that are:
- Stored on-chain and indexed by the API
- Searchable by sender, recipient, reference text, or timestamp
- Useful for accounting, invoicing, and payment tracking
- Supported across all chains where ZCHF is deployed

The Transfers API enables you to:

- Query recent transfers with reference messages
- Search transfers by sender or recipient address
- Filter transfers by reference text (partial matching)
- Track transfers within specific time ranges
- Build complete transfer histories for addresses

## Key Concepts

### Transfer References

A transfer reference is a custom string attached to a ZCHF transfer transaction. Common uses include:
- Invoice numbers: `"Invoice #12345"`
- Payment purposes: `"Salary - December 2024"`
- Order IDs: `"Order-ABC-789"`
- Notes: `"Thanks for the coffee!"`

### Cross-Chain Support

Transfer references work across all chains where ZCHF is deployed:
- The `chainId` field indicates the source chain
- The `targetChain` field indicates the destination chain
- This enables tracking of bridge transfers

### Sequential Counting

Each transfer reference is assigned a unique `count` number, which:
- Increments sequentially for each referenced transfer
- Can be used to retrieve specific transfers by ID
- Helps track the total number of referenced transfers

## Main Endpoints

### List and Count

- `GET /transfer/reference/list` - Get the most recent transfer references
- `GET /transfer/reference/counter` - Get the current count (total number of transfers with references)
- `GET /transfer/reference/by/count/:count` - Retrieve a specific transfer by its count number

### Query by Address

- `GET /transfer/reference/by/from/:from` - Latest transfers sent from an address
- `GET /transfer/reference/by/to/:to` - Latest transfers received by an address
- `GET /transfer/reference/history/by/from/:from` - Complete transfer history sent from an address
- `GET /transfer/reference/history/by/to/:to` - Complete transfer history received by an address

### Query Parameters

All address-based endpoints support optional query parameters:
- `to` / `from` - Filter by the other party in the transaction
- `reference` - Search for transfers containing specific text in the reference
- `start` - Unix timestamp for the beginning of the time range (default: 0)
- `end` - Unix timestamp for the end of the time range (default: current time)

## Use Cases

### Payment Tracking

Track all payments sent or received by an address with reference messages:

```
GET /transfer/reference/by/from/0x963eC454423CD543dB08bc38fC7B3036B425b301
```

### Invoice Verification

Verify that an invoice was paid by searching for the invoice number:

```
GET /transfer/reference/by/from/0x963eC454423CD543dB08bc38fC7B3036B425b301?reference=Invoice%20%2312345
```

### Account Reconciliation

Build a complete payment history for accounting purposes:

```
GET /transfer/reference/history/by/from/0x963eC454423CD543dB08bc38fC7B3036B425b301?start=1704067200&end=1735689600
```

### Payment Explorer

Build a transfer explorer showing recent payments with references:

```
GET /transfer/reference/list
```

### Counterparty Search

Find all transfers between two specific addresses:

```
GET /transfer/reference/by/from/0xabc...?to=0xdef...
```

## Data Structure

### Transfer Reference Object

```json
{
  "amount": "1000000000000000000000",
  "chainId": 1,
  "count": 5234,
  "created": 1768914604,
  "from": "0x963eC454423CD543dB08bc38fC7B3036B425b301",
  "sender": "0x963eC454423CD543dB08bc38fC7B3036B425b301",
  "to": "0x6a4a629d14EC0fc8e2b7DB41949FefaA4F63327F",
  "amount": "1000000000000000000000",
  "reference": "Invoice #12345",
  "targetChain": "1",
  "txHash": "0x1234567890abcdef..."
}
```

### Field Descriptions

- **amount**: Transfer amount (as string in wei, typically 1e18 for ZCHF)
- **chainId**: Source blockchain chain ID
- **count**: Sequential counter for this transfer reference
- **created**: Unix timestamp of the transfer
- **from**: Immediate sender address (may differ from original sender for bridged transfers)
- **sender**: Original sender address
- **to**: Recipient address
- **reference**: Custom reference message (can be empty string)
- **targetChain**: Destination chain ID (for bridge transfers)
- **txHash**: Transaction hash on the source chain

## Understanding Latest vs History

### Latest Endpoints (`/by/from`, `/by/to`)

- Return only the most recent matching transfers
- Optimized for quick lookups
- Useful for displaying recent activity
- Limited results

### History Endpoints (`/history/by/from`, `/history/by/to`)

- Return complete transfer history
- Can be filtered by time range
- Useful for full accounting and reconciliation
- May return larger datasets

## Integration Examples

### Payment Notification System

```javascript
// Poll for new incoming payments
let lastCount = await fetch('https://api.frankencoin.com/transfer/reference/counter')
  .then(r => r.json());

setInterval(async () => {
  const currentCount = await fetch('https://api.frankencoin.com/transfer/reference/counter')
    .then(r => r.json());

  if (currentCount > lastCount) {
    // New transfer(s) occurred
    const transfers = await fetch(`https://api.frankencoin.com/transfer/reference/by/to/${myAddress}`)
      .then(r => r.json());

    transfers.forEach(transfer => {
      if (transfer.count > lastCount) {
        notifyUser(`New payment received: ${transfer.amount / 1e18} ZCHF - ${transfer.reference}`);
      }
    });

    lastCount = currentCount;
  }
}, 10000); // Check every 10 seconds
```

### Invoice Status Checker

```javascript
async function checkInvoicePayment(invoiceNumber, expectedFrom, expectedAmount) {
  const transfers = await fetch(
    `https://api.frankencoin.com/transfer/reference/by/from/${expectedFrom}?reference=${invoiceNumber}`
  ).then(r => r.json());

  const payment = transfers.find(t =>
    t.reference.includes(invoiceNumber) &&
    BigInt(t.amount) >= BigInt(expectedAmount)
  );

  return payment ? 'paid' : 'pending';
}
```

### Account Statement Generator

```javascript
async function generateStatement(address, startDate, endDate) {
  const startTimestamp = Math.floor(startDate.getTime() / 1000);
  const endTimestamp = Math.floor(endDate.getTime() / 1000);

  const sent = await fetch(
    `https://api.frankencoin.com/transfer/reference/history/by/from/${address}?start=${startTimestamp}&end=${endTimestamp}`
  ).then(r => r.json());

  const received = await fetch(
    `https://api.frankencoin.com/transfer/reference/history/by/to/${address}?start=${startTimestamp}&end=${endTimestamp}`
  ).then(r => r.json());

  return {
    sent: sent.map(t => ({
      date: new Date(t.created * 1000),
      to: t.to,
      amount: t.amount / 1e18,
      reference: t.reference,
      txHash: t.txHash
    })),
    received: received.map(t => ({
      date: new Date(t.created * 1000),
      from: t.from,
      amount: t.amount / 1e18,
      reference: t.reference,
      txHash: t.txHash
    }))
  };
}
```

## Notes

### Reference Text Handling

- References can be empty strings (not all transfers include references)
- Reference search is case-sensitive
- Partial matching is supported (searching "Invoice" will match "Invoice #123")
- Special characters should be URL-encoded in query parameters

### Performance Considerations

- Latest endpoints are faster than history endpoints
- Consider caching transfer data for known count ranges
- History endpoints may return large datasets for very active addresses
- Use time range filters to limit result sizes

### Cross-Chain Transfers

- `from` and `sender` may differ for bridged transfers
- `chainId` and `targetChain` indicate bridge operations when they differ
- Same-chain transfers will have identical `chainId` and `targetChain`

### Best Practices

1. **URL Encode**: Always URL-encode reference text in queries
2. **Time Ranges**: Use time ranges to limit history queries
3. **Pagination**: For very active addresses, combine count-based pagination with time ranges
4. **Validation**: Validate address formats before querying
5. **Error Handling**: Handle "Not found" responses gracefully when querying by count
6. **Amount Display**: Always convert amounts from wei (divide by 1e18) for display
7. **Timestamp Conversion**: Convert Unix timestamps to human-readable dates in UI

## Common Patterns

### Finding Payments Between Two Parties

```
GET /transfer/reference/by/from/0xABC...?to=0xDEF...
```

### Searching by Invoice Number

```
GET /transfer/reference/by/from/0xABC...?reference=INV-2024-001
```

### Time-Bound Queries

```
GET /transfer/reference/history/by/from/0xABC...?start=1704067200&end=1735689600
```

### Retrieving Specific Transfer

```
GET /transfer/reference/by/count/5234
```
