from django.contrib import admin

from .models import Talks


class TalksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Talks._meta.fields]


admin.site.register(Talks, TalksAdmin)
