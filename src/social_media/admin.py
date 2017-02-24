import datetime

from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]

    normaluser_fields = ('text', 'photo', 'platforms')
    superuser_fields = ('status',)

    # Visually appealing large textbox.
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 5, 'cols': 60})},
    }

    def get_queryset(self, request):
        """
        Display posts only created by the user, in case the user doesn't have
        superuser permissions.
        """
        queryset = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(created_by_id=request.user.id)

    def get_readonly_fields(self, request, obj=None):
        """
        Disable editing fields when the post is already accepted.
        """
        if obj and obj.status == 'A':
            return self.readonly_fields + self.normaluser_fields + self.superuser_fields
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        """
        Gets the social media post form based on the type of the user.
        """
        if request.user.is_superuser:
            self.fields = self.normaluser_fields + self.superuser_fields
        elif request.user.has_perm('social_media.add_post'):
            self.fields = self.normaluser_fields
        return super(PostAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database, after adding required values.
        """
        if request.user.is_superuser:
            obj.moderated_by = request.user
            obj.moderated_at = datetime.datetime.now()

        elif request.user.has_perm('social_media.add_post'):
            self.set_attr_if_not_set(obj, 'status', 'H')

        self.set_attr_if_not_set(obj, 'created_by', request.user)
        self.set_attr_if_not_set(obj, 'created_at', datetime.datetime.now())
        obj.save()

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Returns the choices for all choice field. It prevents the user to set the status as 'POSTED'
        (by not showing that option).
        """
        if db_field.name == 'status':
            kwargs['choices'] = self.get_required_choices(db_field.choices,
                                                          choices_not_required_set={('P', 'POSTED')})
        return super(PostAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    @staticmethod
    def get_required_choices(choices, choices_not_required_set):
        """ Return a tuple of choices except the one in choices not required."""
        new_choices = ()
        for choice in choices:
            if choice not in choices_not_required_set:
                new_choices += (choice,)
        return new_choices

    @staticmethod
    def set_attr_if_not_set(obj, attr, value):
        """
        Utility method for setting an attribute if the attribute is either None
        or if the Related model doesn't exists in case of the attribute being
        a foreign key to another model.
        """
        if (not hasattr(obj, attr)) or (not getattr(obj, attr)):
            setattr(obj, attr, value)

admin.site.register(Post, PostAdmin)
