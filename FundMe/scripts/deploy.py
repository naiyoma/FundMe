from brownie import FundMe
from .help_scripts import get_account

def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from":account}, publish_source=True)
    # import pdb; pdb.set_trace()

def main():
    deploy_fund_me()
