// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase{
    //user enter the competition
    address payable[] public players;
    address public recentwinnner;
    address public randomness;
    uint256 public entryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    // 0
    // 1
    // 2
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    //set entry fee
    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee;
        bytes32 _keyhash;
    )
        public VRFConsumerBase(_vrfCoordinator, _link) {
        entryFee = 50*(10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }
    function enter() public payable{
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntraceFee(), "Not Enough EHT");
        players.push(msg.sender);
    }
    //user to deposit EtH
    function getEntraceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 new_price = uint256(price) * 10**10;
        uint256 costToEnter = (entryFee * 10**18) / new_price;
        return costToEnter;
    }
    //start the lottery
    function startLottery() public  onlyOwner{
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }
    //end
    function endLottery() public {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
    internal
    override {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You arent there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentwinnner = players[indexOfWinner];
        recentwinnner.transfer(address(this).balance);
        // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;

    }
}
