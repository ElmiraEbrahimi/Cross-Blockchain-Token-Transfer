from web3 import Web3

import os

from core.models import Config


def load_eth_url():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/ETH.txt', 'r') as f:
        url = str(f.read())

    return url


def load_bsc_url():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/BSC.txt', 'r') as f:
        url = str(f.read())

    return url


def get_w3_eth():
    # eth_url = load_eth_url()
    eth_url = Config.objects.get().eth_url
    instance = Web3(Web3.HTTPProvider(eth_url))
    assert instance.is_connected()

    return instance


def get_w3_bsc():
    bsc_url = Config.objects.get().bsc_url
    instance = Web3(Web3.HTTPProvider(bsc_url))
    assert instance.is_connected()

    return instance
