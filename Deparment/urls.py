
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, ClientViewSet, TicketViewSet, TicketResponseViewSet

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    
]
