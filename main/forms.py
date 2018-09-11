# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError

from main.models import *


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)
    sponsor = forms.CharField()
    is_agree = forms.BooleanField()
    region = forms.ChoiceField(choices=(('', '--- Выберите область ---'),) + region_choices)

    class Meta:
        model = User
        fields = (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'sponsor', 'is_agree', 'mobilnik',
            'phone', 'region', 'city')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionKeys
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobilnik', 'phone', 'email')


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

    def get_user(self):
        return User.objects.get(wallet_id=self.cleaned_data['wallet_id'])


class CashRequestsForm(forms.ModelForm):
    class Meta:
        model = CashRequests
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CashRequestsForm, self).__init__(*args, **kwargs)
        # self.fields['points'].empty_label = 'Выберите количество баллов'
        self.fields['points'].choices = ((1000, '1000'), (2000, '2000'))
        # self.fields['points'].widget = forms.RadioSelect
