---
description: Documentation on minting Frankencoins against a collateral.
---

# 🖨️ Collateralized Minting

When someone mints fresh Frankencoins against a collateral, we call the result a [position](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/Position.sol). At the time of writing, the only smart contract that is approved to create new positions is the [minting hub](https://github.com/Frankencoin-ZCHF/FrankenCoin/blob/main/contracts/MintingHub.sol). The notation is inspired by portfolio theory, where a position denotes an exposure to a specific asset. In the Frankencoin system, a position always belongs to exactly one owner. Initially, this is the user that created the position, but ownership is transferable through the standard functions of ownable contracts. The owner can deposit collateral into the position and mint Frankencoins up to a certain limit defined by the liquidation price. Anyone can challenge a position if they believe that the liquidation price is below the true value of the collateral, triggering an auction that serves the purpose of determining the market price of the collateral. Thanks to this mechanism, the Frankencoin does not depend on oracles and is very flexible with regard to the provided collateral.

There are two ways to initiate a position: one can either create a completely new one with arbitrary parameters or one can clone an existing position. The former is for advanced users and not exposed in the default frontend. The latter is the faster way of obtaining Frankencoin against a collateral and supported in the default frontend.
