from django.urls import path
from rest_framework import routers

from accounts.views import (LoginViewSet,
                            RegistrationViewSet,
                            RefreshViewSet,

                            verify_email)
from .views import (WorkerViewSet,
                    ClientViewSet,
                    LocationViewSet,
                    AppointmentViewSet,
                    ScheduleViewSet,
                    ManagerViewSet,
                    )

app_name = 'api'
routes = routers.SimpleRouter()
routes.register('login', LoginViewSet, basename='login')
routes.register('register', RegistrationViewSet, basename='register')
routes.register('auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register('workers', WorkerViewSet, basename='workers')
routes.register('clients', ClientViewSet, basename='clients')
routes.register('locations', LocationViewSet, basename='locations')
routes.register('appointments', AppointmentViewSet, basename='appointments')
routes.register('work_schedules', ScheduleViewSet, basename='work_schedules')
routes.register('managers', ManagerViewSet, basename='managers')

urlpatterns = [
    *routes.urls,
    path('activate/', verify_email, name="email-verify"),

]
