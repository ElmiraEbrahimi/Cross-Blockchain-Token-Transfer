from django.db import models


class Config(models.Model):
    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Configs'

    eth_url = models.URLField(blank=True, null=True)
    bsc_url = models.URLField(blank=True, null=True)

    owner_eth_address = models.CharField(max_length=255, blank=True, null=True)
    owner_bsc_address = models.CharField(max_length=255, blank=True, null=True)

    eth_third_party_address = models.CharField(max_length=255, blank=True, null=True)
    bsc_third_party_address = models.CharField(max_length=255, blank=True, null=True)

    alice_eth_address = models.CharField(max_length=255, blank=True, null=True)
    bob_bsc_address = models.CharField(max_length=255, blank=True, null=True)

    deployed_eth_contract_address = models.CharField(max_length=255, blank=True, null=True)
    deployed_bsc_contract_address = models.CharField(max_length=255, blank=True, null=True)

    is_contract_compiled = models.BooleanField(default=False)

    event_handler_status = models.BooleanField(default=False)

    is_eth_deployed = models.BooleanField(default=False)
    is_bsc_deployed = models.BooleanField(default=False)

    def __str__(self):
        return 'Config'


class Event(models.Model):
    class EventType(models.TextChoices):
        TRANSFER = 'T', 'Transfer'
        APPROVAL = 'A', 'Approval'
        BURNING = 'B', 'Burning'
        MINTING = 'M', 'Minting'

    created_at = models.DateTimeField()
    event_type = models.CharField(choices=EventType.choices, max_length=1)
    payload = models.TextField()
