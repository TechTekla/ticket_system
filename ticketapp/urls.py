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
    path('tickets/', ticket_list, name='ticket_list'),
path('tickets/submit/', submit_ticket, name='submit_ticket'),
path('tickets/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
path('tickets/<int:ticket_id>/update/', update_ticket_status, name='update_ticket'),
]