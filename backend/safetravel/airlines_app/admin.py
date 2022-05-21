from django.contrib import admin
from airlines_app.models import Airline, Plane, Pilot

# Register your models here.
admin.site.register(Airline)
admin.site.register(Plane)
admin.site.register(Pilot)
