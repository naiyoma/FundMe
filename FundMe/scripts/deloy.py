from brownie import FundMe
from scripts.helpful.scripts import get_account

def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from":account})
    import pdb; pdb.set_trace()

def main():
    deploy_fund_me()