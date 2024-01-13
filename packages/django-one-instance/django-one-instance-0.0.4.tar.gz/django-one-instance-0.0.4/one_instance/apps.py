from django.apps import AppConfig


class OneInstanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'one_instance'
