
from django import forms
from .models import Ticket, TicketResponse, Department, Client 
from users.models import User

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_person', 'email', 'phone_number', 'department'] 

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'priority', 'client', 'assigned_to'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all().order_by('name')
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True).order_by('username') 

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ['response_text', 'status']