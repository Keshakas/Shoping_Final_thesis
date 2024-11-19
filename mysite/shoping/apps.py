from django.apps import AppConfig


class ShopingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shoping'

    def ready(self):
        from .signals import create_profile, save_profile
