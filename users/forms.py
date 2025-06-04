from django import forms
from .models import User, GenderChoices

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email', 'gender']
        widgets = {
            'gender': forms.Select(choices=GenderChoices.choices)
        }
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split()) < 2:
            raise forms.ValidationError("Please enter both first and last name")
        return full_name.title()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError("This email is already in use")
        return email.lower()