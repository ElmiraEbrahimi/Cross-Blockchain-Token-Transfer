import json
import os

from web3 import Web3
from web3.contract import Contract
from typing import (
    Type,
    Tuple,
)

from blockchain.utils.load_abi import load_local_abi
from core.models import Config


def get_contract(w3, contract_address) -> Tuple[Type[Contract], Type[Web3]]:
    abi = load_local_abi()
    contract = w3.eth.contract(address=contract_address, abi=abi)

    return contract, w3


def save_bsc_contract_address(contract_address):
    cf = Config.objects.get()
    cf.deployed_bsc_contract_address = contract_address
    cf.is_bsc_deployed = True
    cf.save()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/../contracts/BSC-Address.txt', 'w') as f:
    #     f.write(json.dumps({'deployed_BSC_contract_address': contract_address}))


def save_eth_contract_address(contract_address):
    cf = Config.objects.get()
    cf.deployed_eth_contract_address = contract_address
    cf.is_eth_deployed = True
    cf.save()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/../contracts/ETH-Address.txt', 'w') as f:
    #     f.write(json.dumps({'deployed_ETH_contract_address': contract_address}))


def load_eth_contract_address():
    cf = Config.objects.get()
    address = cf.deployed_eth_contract_address
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/../contracts/ETH-Address.txt', 'r') as f:
    #     address = json.loads(f.read()).get('deployed_ETH_contract_address')

    return address


def load_bsc_contract_address():
    cf = Config.objects.get()
    address = cf.deployed_bsc_contract_address
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/../contracts/BSC-Address.txt', 'r') as f:
    #     address = json.loads(f.read()).get('deployed_BSC_contract_address')

    return address
