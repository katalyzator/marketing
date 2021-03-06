# coding=utf-8
from django.core.exceptions import ValidationError

from main.models import *

from django import forms


class CashRequestAmountSelect(forms.Select):
    # template_name = 'widgets/select_option.html'
    # pass
    option_template_name = 'widgets/select_option.html'


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)
    sponsor = forms.CharField()
    is_agree = forms.BooleanField()

    class Meta:
        model = User
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'sponsor', 'is_agree',
            'passport_id', 'INN',
            'phone', 'region', 'city')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionKeys
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'username', 'last_login', 'date_joined')


class TransferForm(forms.ModelForm):
    wallet_id = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Transfer
        exclude = ('to_user',)

    def clean_wallet_id(self):
        walled_id = self.cleaned_data['wallet_id']
        if User.objects.filter(wallet_id=walled_id).exists():
            return walled_id
        raise ValidationError("Пользователя с таки лицевым счетом, не найдено")

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.cleaned_data['from_user'].points < amount:
            raise ValidationError("У вас недостаточно баллов")
        return amount

    def get_user(self):
        return User.objects.get(wallet_id=self.cleaned_data['wallet_id'])


class CashRequestsForm(forms.ModelForm):
    class Meta:
        model = CashRequests
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CashRequestsForm, self).__init__(*args, **kwargs)
        self.fields['points'].choices = cash_request_choices
