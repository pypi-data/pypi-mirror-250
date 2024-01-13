import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('singleton_pk',)