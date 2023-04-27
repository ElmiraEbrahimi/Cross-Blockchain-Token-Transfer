import binascii

from eth_account import Account

from core.models import Config


def _pk_str_to_bin32(pk: str) -> bytes:
    pk_bin = binascii.unhexlify(pk)
    if len(pk_bin) > 32:
        pk_bin = pk_bin[:32]
    return pk_bin


def load_eth_third_party_address():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/ETH-Third-Party.txt', 'r') as f:
    #     address = f.read()

    return '0x0018F54640da144734eC12429060dF555cbe325F'  # random sample eth address (because there is no need for it!)


def load_bsc_third_party_address():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # with open(dir_path + '/BSC-Third-Party.txt', 'r') as f:
    #     address = f.read()
    cf = Config.objects.get()
    address = cf.bsc_third_party_address
    return address