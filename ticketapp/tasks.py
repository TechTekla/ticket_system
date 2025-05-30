# tasks for background jobs like making old tickets expire
from datetime import timedelta
from django.utils import timezone
from .models import Ticket

def expire_old_tickets():
    old_tickets = Ticket.objects.filter(status='Closed', updated_at__lt=timezone.now() - timedelta(days=30))
    old_tickets.update(is_expired=True)
