#test the conversion of the entry fee
from brownie import Lottery, accounts, config, network
from web3 import web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"], {"from": account},
    )

    assert lottery.getEntraceFee() > web3.toWei(0.019, "ether")
    assert lottery.getEntraceFee() > web3.toWei(0.022, "ether")
