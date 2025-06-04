
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, ClientViewSet, TicketViewSet, TicketResponseViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'ticket-responses', TicketResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
