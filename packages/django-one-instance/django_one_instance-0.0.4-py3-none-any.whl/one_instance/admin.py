from functools import update_wrapper
from django.contrib import admin
from django.core.exceptions import ValidationError


class SingletonAdmin(admin.ModelAdmin):

    change_form_template    = 'one_instance/change_form.html'
    object_history_template = 'one_instance/object_history.html'

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path('', wrap(self.change_view), name='%s_%s_changelist' % info),
            path('history/', wrap(self.history_view), name='%s_%s_history' % info),
            path('change/', wrap(self.change_view), name='%s_%s_change' % info),
        ]

    def get_object(self, request, object_id=None, from_field=None):
        queryset = self.get_queryset(request)
        model = queryset.model
        try:
            return queryset.get()
        except (model.DoesNotExist, ValidationError, ValueError):
            return None

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        object_id = ''
        extra_context = dict(
            show_delete               = False,
            show_save_and_add_another = False,
            show_save_and_continue    = False,
        )
        return self.changeform_view(request, object_id, form_url, extra_context)
    
    def history_view(self, request, object_id=None, extra_context=None):
        object_id = getattr(self.get_object(request), 'pk', None)
        if object_id:
            object_id = str(object_id)
        return super().history_view(request, object_id, extra_context)
