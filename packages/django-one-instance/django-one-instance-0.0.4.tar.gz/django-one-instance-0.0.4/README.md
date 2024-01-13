Django One Instance
===========

[![build-status-image]][build-status]
[![pypi-version]][pypi]
![python-version][python-version]
![django-version][django-version]

Django One Instance is a Django app which enforces the use of a single entry for a given model (i.e.: singleton model). 

The app provides an abstract model to extend which enforces the singleton models behaviour and an admin base class for registering the singleton models in the admin site.

Usage
-----------

Say you have a Config model and you want to enforce its use only with one instance. All you need to to is to extend the SingletonModel abstract model which provides a custom manager for this purpose.

```python
# models.py
from one_instance.models import SingletonModel

class Config(SingletonModel):

    enabled = models.BooleanField()
```

You can also register the model in the django admin and it will be aware that there is only one object.

```python
# admin.py
from django.contrib import admin

from testapp.models import Config
from one_instance.admin import SingletonAdmin


admin.site.register(Config, SingletonAdmin)
```

### New singleton model

```python
from testapp.models import Config
>>> Config.objects.create(enabled=False)
<Config: Config object (1)>
>>> Config.objects.get()
<Config: Config object (1)>
```

Note how you don't have to pass the pk to the get() method. If you try to create another instance you get an error.

```
>>> Config.objects.create(enabled=False)
one_instance.models.SingletonModelAlreadyExists: You are receiving this error after attempting to create another instance of the singleton model. Set DJANGO_ONE_STRICT=False to drop the exception and return the model instance instead.
```

### Pre-existing model
If you extend the SingletonModel for a pre-existing model with many instances, the default get() behaviour is to return the last entry which becames the singleton object. Alternatively, you can explicitly provide the pk of the instance to use with the `Meta` option `singleton_pk`.

```python
class PreExistingModelExample(SingletonModel):

    class Meta:

        singleton_pk = 2
```

```django
>>> PreExistingModelExample.objects.get()
<PreExistingModelExample: PreExistingModelExample object (2)>
```
the other entries are hidden by the manager
```django
>>> PreExistingModelExample.objects.all()
<SingletonModelQuerySet [<PreExistingModelExample: PreExistingModelExample object (2)>]>
>>> PreExistingModelExample.objects.first()
<PreExistingModelExample: PreExistingModelExample object (2)>
>>> PreExistingModelExample.objects.last()
<PreExistingModelExample: PreExistingModelExample object (2)>
```
if you try to forcefully get one of the other instances, you get an error
```
>>> PreExistingModelExample.objects.get(pk=1)
TypeError: You should use get() method without any arguments. Set DJANGO_ONE_STRICT=False if you want to silently drop the unneeded arguments.
```

### Model inheritance
The `objects` manager of the singleton model will include the custom methods from each objects manager of each parent class (if any).

```python
class ManagerA(models.Manager):

    def as_json(self):
        return serializers.serialize("json", self.all())

class ExtraManagerA(models.Model):

    objects = ManagerA()

    class Meta:
        abstract = True

class ModelInheritanceExample(SingletonModel, ExtraManagerA):

    pass
```
```django
>>> models.ModelInheritanceExample.objects.get()
<ModelInheritanceExample: ModelInheritanceExample object (1)>
>>> models.ModelInheritanceExample.objects.as_json()
'[{"model": "testapp.modelinheritanceexample", "pk": 1, "fields": {}}]'
```

Installation
-----------
- `pip install django-one-instance`
- Add "one_instance" to your INSTALLED_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        ...,
        "one_instance",
    ]
    ```

[build-status-image]: https://github.com/federicodabrunzo/django-one-instance/actions/workflows/test-and-publish.yml/badge.svg?branch=dev
[build-status]: https://github.com/federicodabrunzo/django-one-instance/actions/workflows/test-and-publish.yml
[pypi-version]: https://img.shields.io/pypi/v/django-one-instance.svg
[pypi]: https://pypi.org/project/django-one-instance/
[python-version]: https://img.shields.io/pypi/pyversions/django-one-instance
[django-version]: https://img.shields.io/pypi/frameworkversions/django/django-one-instance

