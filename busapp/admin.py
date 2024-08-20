from django.contrib import admin
from .models import Route, Bus, Booking

# Register your models here.
admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Booking)