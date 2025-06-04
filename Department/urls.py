from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_page_html, name='home'),
    path('tickets/', views.get_all_tickets_html, name='all_tickets'),
    path('tickets/<int:ticket_id>/', views.get_ticket_detail_html, name='ticket_detail'),

]
