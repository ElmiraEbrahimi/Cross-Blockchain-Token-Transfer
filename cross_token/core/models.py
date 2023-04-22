import binascii

from django.db import models
from eth_account import Account


class Config(models.Model):
    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Configs'

    eth_url = models.URLField(default='https://rpc2.sepolia.org')
    eth_chain_id = models.PositiveIntegerField(default=11155111)
    bsc_url = models.URLField(default='https://rpc.ankr.com/bsc_testnet_chapel')
    bsc_chain_id = models.PositiveIntegerField(default=97)

    owner_eth_pk = models.CharField(max_length=255,
                                    default='c621a39006eb9aa849870fe48b59a00ffbf35da512f9988e57b3ab234170e53c')
    owner_eth_address = models.CharField(max_length=255)
    alice_eth_pk = models.CharField(max_length=255,
                                    default='bf52d8775356ce13f1f5dd1185e028d08e5edbce0ba2b3cea8e61d4b9c4d0b11')
    alice_eth_address = models.CharField(max_length=255)
    eth_third_party_pk = models.CharField(max_length=255, blank=True, null=True)

    owner_bsc_pk = models.CharField(max_length=255,
                                    default='e258650cd94715d2401382c189f5c8ed606aa2a6f479715e8fdb405301fa78c6')
    owner_bsc_address = models.CharField(max_length=255)
    bob_bsc_pk = models.CharField(max_length=255,
                                  default='4e66338d176e5da27b991b057d57bb61a1d361a9d8c3ef0e5ca78e53509f9c2f')
    bob_bsc_address = models.CharField(max_length=255)
    bsc_third_party_pk = models.CharField(max_length=255,
                                          default='acb5b3b08c3302b117e6ba9d499f37f613eb68406d8f21ef9e94a5c2734325c5')
    bsc_third_party_address = models.CharField(max_length=255)

    deployed_eth_contract_address = models.CharField(max_length=255, blank=True, null=True)
    deployed_bsc_contract_address = models.CharField(max_length=255, blank=True, null=True)

    is_contract_compiled = models.BooleanField(default=False)

    event_handler_status = models.BooleanField(default=False)

    is_eth_deployed = models.BooleanField(default=False)
    is_bsc_deployed = models.BooleanField(default=False)

    @staticmethod
    def _pk_str_to_bin32(pk: str) -> bytes:
        pk_bin = binascii.unhexlify(pk)
        if len(pk_bin) > 32:
            pk_bin = pk_bin[:32]
        return pk_bin

    def save(self, *arg, **kwargs):
        self.owner_eth_address = Account.from_key(self._pk_str_to_bin32(self.owner_eth_pk)).address
        self.alice_eth_address = Account.from_key(self._pk_str_to_bin32(self.alice_eth_pk)).address
        self.owner_bsc_address = Account.from_key(self._pk_str_to_bin32(self.owner_bsc_pk)).address
        self.bob_bsc_address = Account.from_key(self._pk_str_to_bin32(self.bob_bsc_pk)).address
        self.bsc_third_party_address = Account.from_key(self._pk_str_to_bin32(self.bsc_third_party_pk)).address
        super().save(*arg, **kwargs)

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