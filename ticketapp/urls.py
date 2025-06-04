from django.urls import path
from . import views
# your_project_name/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app_name.urls')), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns = [
    path('',)
]