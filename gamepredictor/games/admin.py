from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.GamesList)
admin.site.register(models.GamePredictions)
admin.site.register(models.UserStats)
admin.site.register(models.TeamStats)