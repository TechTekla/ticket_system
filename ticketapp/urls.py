from django.urls import path
from . import views
urlpatterns = [
    path('tickets/', ticket_list, name='ticket_list'),
path('tickets/submit/', submit_ticket, name='submit_ticket'),
path('tickets/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
path('tickets/<int:ticket_id>/update/', update_ticket_status, name='update_ticket'),
]