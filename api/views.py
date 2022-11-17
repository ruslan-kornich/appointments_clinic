from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Worker, Client, Location, Appointment, Schedule
from .permissions import IsManager, IsAdmin, ReadOnly
from .serializers import (WorkerSerializer,
                          ClientSerializer,
                          LocationSerializer,
                          AppointmentSerializer,
                          ScheduleSerializer,
                          UserSerializer, )


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAdmin | ReadOnly]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdmin]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdmin]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdmin | IsManager | ReadOnly]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdmin | ReadOnly]


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_admin:
            return User.objects.all()
        raise ValidationError(
            {'no_rights': 'You have no permission to access this section. Only your manager can do that.'})
