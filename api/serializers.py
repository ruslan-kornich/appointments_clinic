import json
from datetime import datetime
from typing import Union

from django.contrib.auth.models import User, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Location, Worker, Client, Schedule, Appointment

WEEKDAYS = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6
}


def set_or_update_schedule(db_object: Union[Worker, Location], schedules: Union[dict, list]) -> None:
    if isinstance(schedules, dict):
        schedule_obj, created_status = Schedule.objects.get_or_create(
            weekday=WEEKDAYS.get(schedules.get('weekday').lower()),
            from_hour=schedules.get('from_hour'),
            to_hour=schedules.get('to_hour'))

        db_object.work_schedule.clear()
        db_object.work_schedule.add(schedule_obj)

    elif isinstance(schedules, list):
        db_object.work_schedule.clear()
        for sched in schedules:
            schedule_obj, created_status = Schedule.objects.get_or_create(
                weekday=WEEKDAYS.get(sched.get('weekday').lower()),
                from_hour=sched.get('from_hour'),
                to_hour=sched.get('to_hour'))
            db_object.work_schedule.add(schedule_obj)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'pk': instance.pk,
            'weekday': instance.weekdays[instance.weekday][1],
            'from_hour': instance.from_hour,
            'to_hour': instance.to_hour
        }

    def to_internal_value(self, data):
        weekday = WEEKDAYS.get(data.get('weekday').lower())
        from_hour = data.get('from_hour')
        to_hour = data.get('to_hour')

        return {
            'weekday': weekday,
            'from_hour': from_hour,
            'to_hour': to_hour
        }


class LocationSerializer(serializers.ModelSerializer):
    work_schedule = ScheduleSerializer(many=True)

    class Meta:
        model = Location
        fields = ('pk',
                  'name',
                  'address',
                  'work_schedule',
                  )

    def to_internal_value(self, data):

        name = data.get('name')
        address = data.get('address')
        work_schedule = json.loads(data.get('work_schedule'))

        return {'name': name,
                'address': address,
                'work_schedule': work_schedule
                }

    def create(self, validated_data):

        try:
            schedules = validated_data.pop('work_schedule')
            location = Location(**validated_data)
            location.save()
            set_or_update_schedule(location, schedules)

        except ValidationError:
            raise serializers.ValidationError('Sorry, validation error occurred.')

        return location

    def update(self, instance, validated_data):

        try:
            instance.name = validated_data.get('name', instance.name)
            instance.address = validated_data.get('address', instance.address)
            set_or_update_schedule(instance, validated_data.get('work_schedule'))
        except ValidationError:
            raise serializers.ValidationError('Sorry, validation error occurred.')

        instance.save()

        return instance


class WorkerSerializer(serializers.ModelSerializer):
    work_schedule = ScheduleSerializer(many=True)
    available_slots = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Worker
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'phone',
                  'specialty',
                  'available_slots',
                  'work_schedule',
                  )

    def get_available_slots(self, instance) -> list:

        def __generate_slots_range(start: int, stop: int) -> set:

            slots = {f'0{slot}:00' if slot // 10 == 0 else f'{slot}:00' for slot in range(start, stop)}
            return slots

        date = self.context.get('date')

        if date:
            requested_date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            requested_date = datetime.today().date()

        free_slots = set()

        worker_schedules = Schedule.objects.filter(weekday=requested_date.weekday(),
                                                   worker=instance.pk)

        for schedule in worker_schedules:
            slots = __generate_slots_range(schedule.from_hour.hour, schedule.to_hour.hour)
            free_slots.update(slots)

        worker_appointments = Appointment.objects.filter(worker=instance.pk,
                                                         date=requested_date)
        for appointment in worker_appointments:
            booked_slots = __generate_slots_range(appointment.get_hour('start'), appointment.get_hour('end'))
            for slot in booked_slots:
                try:
                    free_slots.remove(slot)
                except KeyError:
                    pass

        return sorted(free_slots)

    def to_internal_value(self, data):

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        specialty = data.get('specialty')
        if data.get('work_schedule'):
            work_schedule = json.loads(data.get('work_schedule'))
        else:
            work_schedule = None

        return {'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'specialty': specialty,
                'work_schedule': work_schedule
                }

    def create(self, validated_data):
        try:
            schedules = validated_data.pop('work_schedule')
            worker = Worker(**validated_data)
            worker.save()
            set_or_update_schedule(worker, schedules)

        except ValidationError:
            raise serializers.ValidationError('Sorry, validation error occurred')

        return worker

    def update(self, instance, validated_data):

        try:
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.phone = validated_data.get('phone', instance.phone)
            instance.specialty = validated_data.get('specialty', instance.specialty)
            set_or_update_schedule(instance, validated_data.get('work_schedule'))
        except ValidationError:
            raise serializers.ValidationError('Sorry, validation error occured.')

        instance.save()

        return instance


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name',
                  'last_name',
                  'phone'
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

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True
        )

        permissions = ['add_appointment',
                       'change_appointment',
                       'view_appointment',
                       'delete_appointment'
                       ]
        for text_perm in permissions:
            permission = Permission.objects.get(codename=text_perm)
            user.user_permissions.add(permission)

        user.save()
        return user
