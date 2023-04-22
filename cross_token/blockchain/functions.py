import binascii

from blockchain.utils.contract_tools import get_contract, load_eth_contract_address, load_bsc_contract_address
from blockchain.utils.get_w3 import get_w3_bsc, get_w3_eth
from core.models import Config


def _pk_str_to_bin32(pk: str) -> bytes:
    pk_bin = binascii.unhexlify(pk)
    if len(pk_bin) > 32:
        pk_bin = pk_bin[:32]
    return pk_bin


class ContractFunctions:

    def __init__(self, is_bsc):
        config = Config.objects.get()
        if is_bsc:
            self.w3 = get_w3_bsc()
            self.contract_address = load_bsc_contract_address()
            self.owner_pk = _pk_str_to_bin32(config.owner_bsc_pk)
            self.owner_address = config.owner_bsc_address
            self.third_party_address = config.bsc_third_party_address
        else:
            self.w3 = get_w3_eth()
            self.contract_address = load_eth_contract_address()
            self.owner_pk = _pk_str_to_bin32(config.owner_eth_pk)
            self.owner_address = config.owner_eth_address
        self.alice_pk = _pk_str_to_bin32(config.alice_eth_pk)
        self.bsc_third_party_pk = _pk_str_to_bin32(config.bsc_third_party_pk)
        self.contract, _ = get_contract(self.w3, self.contract_address)
        self.account = self.owner_address
        self.w3.eth.default_account = self.account

    def initial(self, value: int) -> bool:
        tx = self.contract.functions.initial(value).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
            'gas': 1000000,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.owner_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        return True

    def transfer(self, receipt_address, value) -> bool:
        tx = self.contract.functions.transfer(receipt_address, value).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.owner_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # approve_txn_hash = self.contract.functions.approve(receipt_address, value).transact({'from': self.account})
        # approve_txn_receipt = self.w3.eth.wait_for_transaction_receipt(approve_txn_hash)
        print(tx_receipt)
        return True

    def transfer_from(self, address_from, address_to, value) -> bool:
        tx = self.contract.functions.transferFrom(address_from, address_to, value).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.owner_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        return True

    def approve(self, spender, value):
        tx = self.contract.functions.approve(spender, value).build_transaction({
            'from': self.account,
            'nonce': self.w3.eth.get_transaction_count(self.account),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.owner_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        return True

    def balance_of(self, address):
        res = self.contract.functions.balanceOf(address).call({'from': self.account})
        print(res)
        return res

    def total_supply_amount(self):
        total_supply = self.contract.functions.totalSupplyAmount().call({'from': self.account})
        return total_supply

    def burn(self, outer_to_address, value, contract) -> bool:
        cf = Config.objects.get()
        alice_address = cf.alice_eth_address
        tx = self.contract.functions.burn(outer_to_address, int(value), contract).build_transaction({
            'from': alice_address,
            'nonce': self.w3.eth.get_transaction_count(alice_address),
            'gas': 2000000,
            'gasPrice': self.w3.to_wei('50', 'gwei')
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.alice_pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        return True

    def mint(self, status, address_from, address_to, value, contract) -> bool:
        if status:
            tx = self.contract.functions.mint(status, address_from, address_to, value, contract).build_transaction({
                'from': self.third_party_address,
                'nonce': self.w3.eth.get_transaction_count(self.third_party_address),
                'gas': 2000000,
                'gasPrice': self.w3.to_wei('50', 'gwei')
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.bsc_third_party_pk)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)
            return True
        else:
            print("Error minting.")
            return False


if __name__ == '__main__':
    pass