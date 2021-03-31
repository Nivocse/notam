from django.contrib import admin

from .models import Runway, Notam, Airport

# Register your models here.
admin.site.register(Runway)
admin.site.register(Notam)
admin.site.register(Airport)