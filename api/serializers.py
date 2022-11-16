from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

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

    def create(self, validated_data):
        appointment = Appointment(
            type=validated_data['type'],
            date=validated_data['date'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            worker=validated_data['worker'],
            client=validated_data['client'],
            location=validated_data['location']
        )

        try:
            appointment.clean()
            appointment.save()
        except ValidationError as argument:
            raise serializers.ValidationError(str(argument))

        return appointment

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.date = validated_data.get('date', instance.date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.worker = validated_data.get('worker', instance.worker)
        instance.client = validated_data.get('client', instance.client)
        instance.location = validated_data.get('location', instance.location)

        try:
            instance.clean()
            instance.save()
        except ValidationError as argument:
            raise serializers.ValidationError(str(argument))

        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'id',
                  'password',
                  'repeat_password',
                  )

        read_only_fields = ('id',)

        extra_kwargs = {
            'password': {'write_only': True},
            'repeat_password': {'write_only': True},
        }
