from django import forms


class ApplyCouponForm(forms.Form):
    code = forms.CharField(label='Промокод', max_length=50,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control-clean',
                               'placeholder': 'Введите промокод',
                           }))
