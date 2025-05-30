
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketsystem.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# management/commands/expire_old_tickets.py
from django.core.management.base import BaseCommand
from .ticketapp.models import Ticket
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Expires old tickets after 30 days'

    def handle(self, *args, **kwargs):
        expired = Ticket.objects.filter(updated_at__lt=timezone.now() - timedelta(days=30))
        expired.update(is_expired=True)
        self.stdout.write(f"Expired {expired.count()} tickets.")
