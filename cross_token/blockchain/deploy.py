import binascii

from eth_account import Account

from blockchain.utils.contract_tools import save_bsc_contract_address, save_eth_contract_address
from blockchain.utils.get_w3 import get_w3_eth, get_w3_bsc
from blockchain.utils.load_abi import load_local_abi
from blockchain.utils.load_bytecode import load_local_bytecode
from blockchain.utils.load_third_party import load_eth_third_party_address, load_bsc_third_party_address
from core.models import Config


def _pk_str_to_bin32(pk: str) -> bytes:
    pk_bin = binascii.unhexlify(pk)
    if len(pk_bin) > 32:
        pk_bin = pk_bin[:32]
    return pk_bin


def deploy_eth_contract():
    w3 = get_w3_eth()
    abi = load_local_abi()
    bytecode = load_local_bytecode()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    owner_pk_str = Config.objects.get().owner_eth_pk
    owner_pk = _pk_str_to_bin32(owner_pk_str)
    account = Account.from_key(owner_pk).address
    w3.eth.default_account = account
    eth_third_party_address = load_eth_third_party_address()

    tx = contract.constructor(eth_third_party_address).build_transaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=owner_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    save_eth_contract_address(contract_address)

    print('Successfully deployed ETH contract')
    return True, contract_address


def deploy_bsc_contract():
    w3 = get_w3_bsc()
    abi = load_local_abi()
    bytecode = load_local_bytecode()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    owner_pk_str = Config.objects.get().owner_bsc_pk
    owner_pk = _pk_str_to_bin32(owner_pk_str)
    account = Account.from_key(owner_pk).address
    w3.eth.default_account = account
    bsc_third_party_address = load_bsc_third_party_address()

    tx = contract.constructor(bsc_third_party_address).build_transaction({
        'from': account,
        'nonce': w3.eth.get_transaction_count(account),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=owner_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    save_bsc_contract_address(contract_address)

    print('Successfully deployed BSC contract')
    return True, contract_address


def contract_exists(is_bsc: bool, contract_address: str):
    if not is_bsc:
        w3 = get_w3_eth()
    else:
        w3 = get_w3_bsc()

    bytecode = w3.eth.get_code(contract_address)
    if bytecode:
        print("Contract is deployed at address", contract_address)
        return True
    else:
        print("No contract is deployed at address", contract_address)
        return False


if __name__ == '__main__':
    deploy_eth_contract()
    deploy_bsc_contract()