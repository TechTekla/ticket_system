from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Ticket

class TicketTestCase(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client1', password='testpass')
        self.staff_user = User.objects.create_user(username='ictstaff', password='testpass', is_staff=True)
        self.ticket = Ticket.objects.create(
            subject='Test Subject',
            description='Test Description',
            priority='High',
            department='IT',
            client=self.client_user
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.subject, 'Test Subject')
        self.assertEqual(self.ticket.status, 'Open')

    def test_ticket_list_view_as_client(self):
        c = Client()
        c.login(username='client1', password='testpass')
        response = c.get('/tickets/')  # Adjust URL to match your urls.py
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Subject')

    def test_ticket_update_by_staff(self):
        c = Client()
        c.login(username='ictstaff', password='testpass')
        response = c.post(f'/tickets/{self.ticket.id}/update/', {
            'status': 'Resolved'
        })
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'Resolved')
