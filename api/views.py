from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Worker, Client, Location, Appointment, Schedule
from .serializers import (WorkerSerializer,
                          ClientSerializer,
                          LocationSerializer,
                          AppointmentSerializer,
                          ScheduleSerializer,
                          UserSerializer, )


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        raise ValidationError(
            {'no_rights': 'You have no permission to access this section. Only your manager can do that.'})
