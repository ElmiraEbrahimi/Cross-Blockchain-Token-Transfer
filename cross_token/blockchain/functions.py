from blockchain.utils.contract_tools import get_contract, load_eth_contract_address, load_bsc_contract_address
from blockchain.utils.get_w3 import get_w3_bsc, get_w3_eth
from core.models import Config


class ContractFunctions:

    def __init__(self, is_bsc):
        config = Config.objects.get()
        if is_bsc:
            self.w3 = get_w3_bsc()
            self.contract_address = load_bsc_contract_address()
            self.third_party_address = config.bsc_third_party_address
        else:
            self.w3 = get_w3_eth()
            self.contract_address = load_eth_contract_address()
            self.third_party_address = config.eth_third_party_address
        self.contract, _ = get_contract(self.w3, self.contract_address)
        self.account = self.w3.to_checksum_address(self.third_party_address)  # TODO: address str? no effect?
        self.w3.eth.default_account = self.account

    def initial(self, value: int) -> bool:
        tx_hash = self.contract.functions.initial(value).transact({'from': self.account})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)
        return True

    def transfer(self, receipt_address, value) -> bool:
        txn_hash = self.contract.functions.transfer(receipt_address, value).transact({'from': self.account})
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        approve_txn_hash = self.contract.functions.approve(receipt_address, value).transact({'from': self.account})
        approve_txn_receipt = self.w3.eth.wait_for_transaction_receipt(approve_txn_hash)
        print(approve_txn_receipt)
        return True

    def transfer_from(self, address_from, address_to, value) -> bool:
        txn_hash = self.contract.functions.transferFrom(address_from, address_to, value).transact(
            {'from': self.account})
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_receipt)
        return True

    def balance_of(self, address):
        res = self.contract.functions.balanceOf(address).call({'from': self.account})
        print(res)
        return res

    def burn(self, outer_to_address, value, token_address) -> bool:
        txn_hash = self.contract.functions.burn(outer_to_address, value, token_address).transact({'from': self.account})
        txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_receipt)
        return True

    def mint(self, status, address_from, address_to, address_value, address_token) -> bool:
        if status:
            txn_hash = self.contract.functions.mint(status, address_from, address_to, address_value,
                                                    address_token).transact({'from': self.account})
            txn_receipt = self.w3.eth.wait_for_transaction_receipt(txn_hash)
            print(txn_receipt)
            return True
        else:
            print("Error!")
            return False


if __name__ == '__main__':
    pass
