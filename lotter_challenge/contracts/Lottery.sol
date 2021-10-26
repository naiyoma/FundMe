// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    //user enter the competition
    address payable[] public players;
    uint256 public entryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    //set entry fee
    constructor(address _priceFeedAddress) public {
        entryFee = 50*(10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }
    function enter() public {
        players.push(msg.sender);
    }
    //user to deposit EtH
    function getEntraceFee() pubic view returns (uint256) {
        (, int256 price, , , ,) = ethUsdPriceFeed.latestRoundData;
        uint256 new_price = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntry * 10**18) / price;
        return costToEntre;
    }
    //start the lottery
    function endLottery() public {}
    //end
    function endLottery() public {}
}
