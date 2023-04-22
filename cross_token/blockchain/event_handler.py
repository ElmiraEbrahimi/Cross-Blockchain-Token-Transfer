import json

import requests
from web3 import Web3

from blockchain.utils.load_abi import load_local_abi


def run_event_handler():
    submit_event_url = 'http://127.0.0.1:8000/submit_event/'
    response = requests.get('http://127.0.0.1:8000/get_w3_and_contract_addresses/', timeout=200)
    print(response)
    print(response.text)
    data = response.json()

    eth_w3_url = data['eth_w3_url']
    eth_w3 = Web3(Web3.HTTPProvider(eth_w3_url))

    bsc_w3_url = data['bsc_w3_url']
    bsc_w3 = Web3(Web3.HTTPProvider(bsc_w3_url))

    eth_contract_address = data['eth_contract_address']
    bsc_contract_address = data['bsc_contract_address']
    abi = load_local_abi()
    eth_contract = eth_w3.eth.contract(address=eth_contract_address, abi=abi)
    bsc_contract = bsc_w3.eth.contract(address=bsc_contract_address, abi=abi)

    transfer_filter = eth_contract.events.Transfer.create_filter(fromBlock='latest')
    approval_filter = eth_contract.events.Approval.create_filter(fromBlock='latest')
    burning_filter = eth_contract.events.Burning.create_filter(fromBlock='latest')
    minting_filter = bsc_contract.events.Minting.create_filter(fromBlock='latest')

    def handle_transfer(event):
        pass

    def handle_approval(event):
        pass

    def handle_burning(event):
        payload = dict(event['args'])
        data = {
            'event_type': 'B',
            'payload': json.dumps(payload)
        }
        res = requests.post(submit_event_url, data=data)
        if res.status_code == 201:
            print("Burning event submitted successfully")

    def handle_minting(event):
        payload = dict(event['args'])
        data = {
            'event_type': 'M',
            'payload': json.dumps(payload)
        }
        res = requests.post(submit_event_url, data=data)
        if res.status_code == 201:
            print("Minting event submitted successfully")

    res = requests.get('http://127.0.0.1:8000/set_event_handler_status_true/')
    if res and res.status_code == 200:
        print('Running event-handler...')
    while True:
        for event in transfer_filter.get_new_entries():
            print(event)
            handle_transfer(event)

        for event in approval_filter.get_new_entries():
            print(event)
            handle_approval(event)

        for event in burning_filter.get_new_entries():
            print(event)
            handle_burning(event)

        for event in minting_filter.get_new_entries():
            print(event)
            handle_minting(event)


if __name__ == '__main__':
    run_event_handler()