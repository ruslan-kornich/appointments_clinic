from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (WorkerViewSet,
                    ClientViewSet,
                    LocationViewSet,
                    AppointmentViewSet,
                    ScheduleViewSet,
                    ManagerViewSet
                    )

#app_name = 'api'
routes = routers.SimpleRouter()
routes.register('workers', WorkerViewSet, basename='workers')
routes.register('clients', ClientViewSet, basename='clients')
routes.register('locations', LocationViewSet, basename='locations')
routes.register('appointments', AppointmentViewSet, basename='appointments')
routes.register('work_schedules', ScheduleViewSet, basename='work_schedules')
routes.register('managers', ManagerViewSet, basename='managers')

urlpatterns = [
    *routes.urls,
    path('login/', TokenObtainPairView.as_view(), name='login_url'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
