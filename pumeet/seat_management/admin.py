from django.contrib import admin

from . import models

admin.site.register(models.Branch)
admin.site.register(models.Preference)