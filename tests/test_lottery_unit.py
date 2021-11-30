from brownie import exceptions, network  # type: ignore
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
)


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
        lottery.enter(
            {"from": get_account(), "value": lottery.getEntranceFee() + 10 ** 8}
        )
    except exceptions.VirtualMachineError:
        exception_raised = True
    assert exception_raised == True


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    account = get_account()
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    value = lottery.getEntranceFee() + 10 ** 8
    lottery.enter({"from": account, "value": value})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    account = get_account()
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10 ** 8})
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    account = get_account()
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10 ** 8})
    lottery.enter(
        {"from": get_account(index=1), "value": lottery.getEntranceFee() + 10 ** 8}
    )
    lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee() + 10 ** 8}
    )
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    request_id = tx.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, 1, lottery.address
    )
    starting_balance_of_acc = get_account(index=1).balance()
    lottery_balance = lottery.balance()

    assert lottery.recentWinner() == get_account(index=1)
    assert lottery.balance() == 0
    assert get_account(index=1).balance() == starting_balance_of_acc + lottery_balance
