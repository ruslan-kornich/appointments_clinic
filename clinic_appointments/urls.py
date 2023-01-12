from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as doc_urls

app_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls'))
]
urlpatterns += doc_urls
