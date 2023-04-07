from blockchain.utils.contract_tools import save_bsc_contract_address, save_eth_contract_address
from blockchain.utils.get_w3 import get_w3_eth, get_w3_bsc
from blockchain.utils.load_abi import load_local_abi
from blockchain.utils.load_bytecode import load_local_bytecode
from blockchain.utils.load_third_party import load_eth_third_party_address, load_bsc_third_party_address


def deploy_eth_contract():
    w3 = get_w3_eth()
    abi = load_local_abi()
    bytecode = load_local_bytecode()
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    account = w3.eth.accounts[0]
    w3.eth.default_account = account
    eth_third_party_address = load_eth_third_party_address()

    tx_hash = contract.constructor(eth_third_party_address).transact()
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
    account = w3.eth.accounts[0]
    w3.eth.default_account = account
    bsc_third_party_address = load_bsc_third_party_address()

    tx_hash = contract.constructor(bsc_third_party_address).transact()
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
