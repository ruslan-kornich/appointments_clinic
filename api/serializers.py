from rest_framework import serializers

from .models import Worker, Client, Location, Appointment, Schedule


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'phone',
                  'specialty',
                  'work_schedule',
                  )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'phone'
                  )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('pk',
                  'name',
                  'address'
                  )


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('pk',
                  'type',
                  'date',
                  'start_time',
                  'end_time',
                  'worker',
                  'client',
                  'location'
                  )


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


