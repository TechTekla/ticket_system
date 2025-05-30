from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    ticket_id = models.IntegerField()  # Change to ForeignKey if you have a Ticket model
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} (from {self.sender.username} to {self.receiver.username})"
