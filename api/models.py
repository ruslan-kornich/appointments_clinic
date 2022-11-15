from django.db import models
from django.utils.timezone import localdate, localtime


class Schedule(models.Model):
    weekdays = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    weekday = models.IntegerField(choices=weekdays, default='Monday')
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    workers = models.ManyToManyField('Worker', blank=True)
    locations = models.ManyToManyField('Location', blank=True)

    def __str__(self):
        return f'{self.weekdays[self.weekday][1]}: {self.from_hour}—{self.to_hour}'


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=600)
    work_schedule = models.ManyToManyField(Schedule, blank=True)

    def __str__(self):
        return f'{self.name}- {self.address}'


class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    work_schedule = models.ManyToManyField(Schedule, blank=True)

    def __str__(self):
        return f'{self.specialty} — {self.first_name} {self.last_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Appointment(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(default=localdate, blank=False)
    start_time = models.TimeField(default=localtime, blank=False)
    end_time = models.TimeField(default=localtime, blank=False)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.date}- {self.start_time} - {self.end_time} '
