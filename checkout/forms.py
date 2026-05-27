from django import forms
from .models import DeliveryAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = [
            'address_type', 'recipient_name', 'phone',
            'city', 'street', 'house', 'apartment', 'postal_code',
            'cdek_pvz_code', 'cdek_pvz_address',
        ]
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': 'Иванов Иван'}),
            'phone': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': '+7 (999) 123-45-67'}),
            'city': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': 'Москва'}),
            'street': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': 'ул. Тверская'}),
            'house': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': '12'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': '45'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': '101000'}),
            'cdek_pvz_code': forms.HiddenInput(),
            'cdek_pvz_address': forms.HiddenInput(),
            'address_type': forms.HiddenInput(),
        }
        labels = {
            'recipient_name': 'Получатель',
            'phone': 'Телефон',
            'city': 'Город',
            'street': 'Улица',
            'house': 'Дом',
            'apartment': 'Квартира',
            'postal_code': 'Индекс',
        }


class CdekAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['address_type', 'recipient_name', 'phone', 'cdek_pvz_code', 'cdek_pvz_address']
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': 'Иванов Иван'}),
            'phone': forms.TextInput(attrs={'class': 'form-control-clean', 'placeholder': '+7 (999) 123-45-67'}),
            'cdek_pvz_code': forms.HiddenInput(),
            'cdek_pvz_address': forms.HiddenInput(),
            'address_type': forms.HiddenInput(),
        }
        labels = {
            'recipient_name': 'Получатель',
            'phone': 'Телефон',
        }
