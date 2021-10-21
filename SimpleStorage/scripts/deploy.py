import os
from brownie import accounts

def deploy_simple_storage():
    # account = accounts.load("naiyoma-account")
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    import pdb; pdb.set_trace()

def main():
    deploy_simple_storage()
