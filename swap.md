---
description: >-
  Simple contracts that allow swapping other Swiss franc stablecoins into
  Frankencoin and back.
---

# 🌁 Stablecoin Bridges

The [Swap page](https://app.frankencoin.com/swap) allows users to exchange recognized Swiss franc stablecoins for Frankencoins and vice versa. Note that this bridge will cease to exist on the 26th of October.&#x20;

The ability to move back into other stablecoins is only possible as long as there are sufficient amounts of those stablecoins left in the bridge contract. This functionality essentially pegs the Frankencoin 1:1 to other stablecoins, helping stabilize its value. The peg ensures that Frankencoin can always be redeemed for an equivalent amount of recognized stablecoins, which helps maintaining trust in its value.

To protect the Frankencoin from a crash of the connected stablecoins, the bridge contract is limited in both time and volume. The contract is designed to be replaced with a new one at least every year. This time limitation ensures that the system can adapt to any changes or instabilities in the connected stablecoins, providing a safeguard against prolonged exposure to potential risks.

System participants should closely monitor the amount of other stablecoins flowing in and out of the bridge contract. This flow of stablecoins can provide important signals about the state of the Frankencoin market. A significant outflow of stablecoins from the bridge contract could indicate that it is too cheap to mint Frankencoins, suggesting that the implied interest rates are too low. Conversely, large inflows of stablecoins into the bridge contract could indicate that holding Frankencoins is too attractive, with interest rates being too high. This could result in an over-demand for Frankencoins, potentially leading to supply shortages or other market distortions.

The bridge contract has volume limits to prevent excessive exposure to any single stablecoin. By capping the amount of stablecoins that can be swapped, the system mitigates the risk of a crash or devaluation of the connected stablecoins affecting the Frankencoin's stability. The annual renewal of the bridge contract is a critical risk management tool. By reviewing and potentially updating the contract terms yearly, the system can respond to changes in the market conditions or in the stability of the connected stablecoins. This proactive approach ensures that the Frankencoin system remains robust and adaptable to external influences.

The system emphasizes transparency, which helps participants make informed decisions and increases trust in the system's stability and governance.
