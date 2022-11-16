from django.contrib import admin

from .models import Client, Schedule, Worker, Location, Appointment

# Register your models here.
admin.site.register(Client)
admin.site.register(Schedule)
admin.site.register(Worker)
admin.site.register(Location)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('type',
                    'worker',
                    'location',
                    'client',
                    'date',
                    'start_time',
                    'end_time',
                    )
