from django.db import models


class Config(models.Model):
    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Configs'

    eth_url = models.URLField(blank=True, null=True)
    bsc_url = models.URLField(blank=True, null=True)

    eth_third_party_address = models.CharField(max_length=255, blank=True, null=True)
    bsc_third_party_address = models.CharField(max_length=255, blank=True, null=True)

    alice_eth_address = models.CharField(max_length=255, blank=True, null=True)
    bob_bsc_address = models.CharField(max_length=255, blank=True, null=True)

    deployed_eth_contract_address = models.CharField(max_length=255, blank=True, null=True)
    deployed_bsc_contract_address = models.CharField(max_length=255, blank=True, null=True)
    is_contract_compiled = models.BooleanField(default=False)
    is_eth_deployed = models.BooleanField(default=False)
    is_bsc_deployed = models.BooleanField(default=False)

    def __str__(self):
        return 'Config'
