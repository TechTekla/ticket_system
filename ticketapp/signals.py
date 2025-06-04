# signals for automations like notifications
# 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from django.core.mail import send_mail

@receiver(post_save, sender=Ticket)
def notify_user_on_ticket_resolution(sender, instance, **kwargs):
    if instance.status == 'Resolved':
        send_mail(
            'Your IT Ticket Has Been Resolved',
            f'Hello, your ticket "{instance.subject}" has been marked as resolved.',
            'support@yourcompany.com',
            [instance.created_by.email]
        )
