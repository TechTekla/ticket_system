from django.db import models
from users.models import User 
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Client(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

class Ticket(models.Model):
    
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tickets')
    
    status = models.CharField(max_length=50, default='Open', choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket #{self.id}: {self.subject}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    responded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], default='Open')

    def __str__(self):
        return f"Response to Ticket #{self.ticket.id} by {self.responded_by.username}"