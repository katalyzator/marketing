# coding=utf-8
from django import forms

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
        exclude = ('is_confirmed_by_user', 'is_confirmed_by_admin')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobilnik', 'phone', 'email')
