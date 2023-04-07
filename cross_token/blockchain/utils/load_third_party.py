import os

from core.models import Config


def load_eth_third_party_address():

    address = Config.objects.get().eth_third_party_address
    return address


def load_bsc_third_party_address():

    address = Config.objects.get().bsc_third_party_address
    return address
