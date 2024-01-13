import inspect
import logging

from types import MethodType

from django.db import models
from django.db.models.base import ModelBase
from django.conf import settings

logger = logging.getLogger(__name__)


class SingletonModelBase(ModelBase):

    @classmethod
    def _get_to_copy_queryset_methods(cls, new_qs, queryset_class):

        new_methods = {}
        for name, method in inspect.getmembers(
                queryset_class, predicate=inspect.isfunction
            ):
            # Only copy missing methods.
            if hasattr(new_qs, name):
                continue

            # Only copy public methods or methods with the attribute `queryset_only=False`.
            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None and name.startswith('_')):
                continue

            new_methods[name] = method
        
        return new_methods

    @classmethod
    def __prepare__(metacls, name, bases, **kwargs):

        logger.debug(f'Preparing {name} class')

        # Creates an 'objects' manager which includes the methods
        # from each objects manager of each parent class (if any)

        attrs = super().__prepare__(metacls, name, bases, **kwargs)
        objects = SingletonModelManager.from_queryset(SingletonModelQuerySet)()
        objects_qs = objects._queryset_class

        for b in bases:            
            if type(b) == ModelBase and 'objects' in b.__dict__:
                b_objects = b._meta.managers_map['objects']
                for name, method in inspect.getmembers(
                    b_objects, predicate=inspect.ismethod
                ):
                    # Only copy missing methods.
                    if hasattr(objects, name):
                        continue

                    logger.debug(
                        f'Copying {name} method from {b.__name__} onto the manager')

                    # Copy the method onto the manager.
                    method.__func__.__qualname__ = \
                        f'{type(objects).__name__}.{name}'
                    setattr(objects, name, MethodType(method.__func__, objects))

                    # If the base class objects manager has a custom queryset
                    # we need to copy its methods on the new objects queryset

                    if not hasattr(b_objects, '_queryset_class'):
                        continue

                    to_copy = metacls._get_to_copy_queryset_methods(
                        objects_qs, b_objects._queryset_class).items()
                    for k, v in to_copy:
                        logger.debug(
                            f'Copying {name} method from '
                            f'{b_objects._queryset_class.__name__} onto the queryset')
                        setattr(objects_qs, k, v)

        attrs.update(objects=objects)
        return attrs


class SingletonModelAlreadyExists(Exception):

    pass


class SingletonModelQuerySet(models.QuerySet):

    DJANGO_ONE_STRICT_DEFAULT = True
    _get_strict_error_msg = 'You should use get() method without any arguments'

    @property
    def _strict(self):
        return getattr(settings, 'DJANGO_ONE_STRICT', 
                       self.DJANGO_ONE_STRICT_DEFAULT)

    def get_instance(self):
        instance = super().last()
        if instance is None:
            raise self.model.DoesNotExist
        return instance

    def get(self, *args, **kwargs):
        if len(args) > 0 or len(kwargs) > 0:
            if self._strict:
                raise TypeError(
                    f'{self._get_strict_error_msg}. Set DJANGO_ONE_STRICT=False '
                    'if you want to silently drop the unneeded arguments.')
            else:
                logger.warning(self._get_strict_error_msg)
        return self.get_instance()

    def create(self, **kwargs):
        if self.count() > 0:
            if self._strict:
                raise SingletonModelAlreadyExists(
                    'You are receiving this error after attempting to create another '
                    'instance of the singleton model. Set DJANGO_ONE_STRICT=False '
                    'to drop the exception and return the model instance instead.')
            logger.warning('model instances already exist, returning last instance')
            return self.get_instance()

        obj = super().create(**kwargs)
        logger.debug(f"created object with pk {obj.pk}")
        return obj
    
    def first(self):
        return self.last()

    def last(self):
        try:
            return self.get_instance()
        except self.model.DoesNotExist:
            return None
        


    #########################
    # NOT SUPPORTED METHODS #
    #########################

    aggregate   = None
    bulk_create = None
    bulk_update = None
    in_bulk     = None


class SingletonModelManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()

        if getattr(self.model._meta, 'singleton_pk', None) is not None:
            qs = qs.filter(pk__in=[self.model._meta.singleton_pk])
        else:
            qs = qs.order_by('-pk')[0:1]
        return super().get_queryset().filter(pk__in=qs)
    

class SingletonModel(models.Model, metaclass=SingletonModelBase):

    class Meta:
        abstract = True
        
