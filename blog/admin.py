from django.contrib import admin
from blog import models

# Register your models here.

admin.site.register(models.Toolbar)
admin.site.register(models.Advertise)
admin.site.register(models.Banner)