from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control-clean', 'placeholder': 'email@example.com'}),
            'subject': forms.Select(attrs={'class': 'form-control-clean'}),
            'message': forms.Textarea(attrs={'class': 'form-control-clean', 'placeholder': 'Ваше сообщение...', 'rows': 5}),
        }
