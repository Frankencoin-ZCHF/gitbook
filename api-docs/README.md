# 📡 Developers

The Frankencoin API provides comprehensive access to all data within the Frankencoin ecosystem. This RESTful API enables developers to integrate Frankencoin functionality into their applications, build analytics tools, monitor positions, and interact with the protocol programmatically.

## Base URL

```
https://api.frankencoin.com
```

## API Features

The Frankencoin API is organized into several controllers, each serving specific data about different aspects of the ecosystem:

### Core Controllers

* [**Ecosystem**](ecosystem.md) - Get information about the Frankencoin token, FPS, minters, and collateral
* [**Positions**](positions.md) - Manage and query collateralized lending positions
* [**Challenges**](challenges.md) - Access liquidation challenge and auction data
* [**Prices**](prices.md) - Access price feeds and historical price data for collateral assets
* [**Savings**](savings.md) - Query savings module data, interest rates, and yields
* [**Transfers**](transfers.md) - Track ZCHF transfers with custom reference messages
* [**Analytics**](analytics.md) - Retrieve ecosystem-wide metrics and financial analytics

## Response Format

In general API responses are returned in JSON format. Most list endpoints follow a consistent structure:

```json
{
  "num": 100,
  "list": [...]
}
```

or

```json
{
  "num": 100,
  "addresses": [...],
  "map": {...}
}
```

## Data Precision

Financial amounts in the API are typically represented as strings to preserve precision:

* Token amounts are in **wei** (1e18 precision for 18-decimal tokens)
* Timestamps are **Unix epoch** (seconds)
* Interest rates are in **PPM** (parts per million, e.g., 20000 = 2%)

## Interactive Documentation

For interactive API exploration with request/response examples, visit the Swagger documentation:

```
https://api.frankencoin.com
```

## Rate Limiting

The API currently has no rate limiting, but please use reasonable request rates to ensure fair access for all users.

## Support

For API questions or issues:

* GitHub Smart Contracts: [Frankencoin ZCHF](https://github.com/Frankencoin-ZCHF/FrankenCoin)
* GitHub API NestJS: [Frankencoin API](https://github.com/Frankencoin-ZCHF/frankencoin-api)
* NPM Package for ABIs, Addresses, SupportedChains, ...: [NPM Package Core](https://www.npmjs.com/package/@frankencoin/zchf)
* NPM Package for API Types, Return Types, ...: [NPM Package API Types](https://www.npmjs.com/package/@frankencoin/api)
* Swagger Docs: [api.frankencoin.com](https://api.frankencoin.com)
