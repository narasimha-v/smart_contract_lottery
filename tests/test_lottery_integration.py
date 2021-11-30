import time

from brownie import network  # type: ignore
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)


def test_can_pick_winner_rink():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10 ** 8})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
