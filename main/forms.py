from django import forms

from main.models import *


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionKeys
        exclude = ('is_confirmed',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'mobilnik', 'phone', 'email')