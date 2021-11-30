import time

from brownie import Lottery, config, network  # type: ignore

from scripts.helpful_scripts import fund_with_link, get_accout, get_contract


def deploy_lottery():
    account = get_accout()
    Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def start_lottery():
    account = get_accout()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started!")


def enter_lottery():
    account = get_accout()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10 ** 8
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("Entered lottery!")


def end_lottery():
    account = get_accout()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    time.sleep(60)
    print(f"Entered lottery! {lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
