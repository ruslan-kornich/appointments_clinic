from django.contrib import admin

from .models import Location, Worker, Client, Schedule, Appointment

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
