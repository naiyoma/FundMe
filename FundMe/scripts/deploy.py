from brownie import FundMe, network, config
from .help_scripts import get_account

def deploy_fund_me():
    account = get_account()
    if network.show_active() != "development":
        price_feed = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    fund_me = FundMe.deploy(
        price_feed,
        {"from": account},
        publish_source=True)
    # import pdb; pdb.set_trace()

def main():
    deploy_fund_me()
