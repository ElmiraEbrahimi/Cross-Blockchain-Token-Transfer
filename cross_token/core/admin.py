from django.contrib import admin
from .models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    fields = (
        'eth_url',
        'bsc_url',
        'owner_eth_address',
        'owner_bsc_address',
        'alice_eth_address',
        'bob_bsc_address',
        'bsc_third_party_address',
        'deployed_eth_contract_address',
        'deployed_bsc_contract_address',
        'is_contract_compiled',
        'is_eth_deployed',
        'is_bsc_deployed',
        'event_handler_status',
    )
    list_display = (
        'eth_url',
        'bsc_url',
        'owner_eth_address',
        'owner_bsc_address',
        'alice_eth_address',
        'bob_bsc_address',
        'bsc_third_party_address',
        'deployed_eth_contract_address',
        'deployed_bsc_contract_address',
        'is_contract_compiled',
        'is_eth_deployed',
        'is_bsc_deployed',
    )
    list_display_links = (
        'eth_url',
        'bsc_url',
        'owner_eth_address',
        'owner_bsc_address',
        'alice_eth_address',
        'bob_bsc_address',
        'bsc_third_party_address',
        'deployed_eth_contract_address',
        'deployed_bsc_contract_address',
        'is_contract_compiled',
        'is_eth_deployed',
        'is_bsc_deployed',
    )
    readonly_fields = (
        'deployed_eth_contract_address',
        'deployed_bsc_contract_address',
        'is_contract_compiled',
        'is_eth_deployed',
        'is_bsc_deployed',
        'event_handler_status',
    )
