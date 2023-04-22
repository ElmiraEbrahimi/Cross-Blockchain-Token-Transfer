from django.apps import AppConfig
from django.contrib.auth import get_user_model


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.models import Config

        try:
            if not get_user_model().objects.filter(username='admin'):
                user = get_user_model().objects.create(username='admin', is_staff=True, is_superuser=True)
                user.set_password('admin')
                user.save()

            if not Config.objects.exists():
                config = Config.objects.create()

            config = Config.objects.get()
            config.eth_third_party_pk = '0x0018F54640da144734eC12429060dF555cbe325F'  # some random address
            config.event_handler_status = False
            config.save()

        except Exception:
            pass