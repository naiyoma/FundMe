from brownie import SimpleStorage, accounts

def test_deploy():
    account = accounts[0]

    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    assert starting_value == expected
