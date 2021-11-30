from brownie import network, exceptions  # type: ignore
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    assert lottery.getEntranceFee() == 25 * (10 ** 15)


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    exception_raised = False
    try:
        value = lottery.getEntranceFee() + 10 ** 8
        lottery.enter({"from": get_account(), "value": value})
    except exceptions.VirtualMachineError:
        exception_raised = True
    assert exception_raised == True
