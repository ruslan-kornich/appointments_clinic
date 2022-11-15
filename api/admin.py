from django.contrib import admin
from .models import Client, Schedule, Worker, Location
# Register your models here.
admin.site.register(Client)
admin.site.register(Schedule)
admin.site.register(Worker)
admin.site.register(Location)