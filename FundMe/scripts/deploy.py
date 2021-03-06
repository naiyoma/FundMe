from brownie import FundMe, network, config, MockV3Aggregator
from .help_scripts import get_account


def deploy_fund_me():
    account = get_account()
    if network.show_active() != "development":
        price_feed = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print("The active network is active")
        print("deploy mocks......")
        mock_aggregator = MockV3Aggregator.deploy(
            10, 2000000000000000000, {"from": account})
        price_feed_address = mock_aggregator.address
        print("Mocks Deployed")

    fund_me = FundMe.deploy(
        price_feed,
        {"from": account},
        publish_source=True)


def main():
    deploy_fund_me()
