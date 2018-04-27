# coding=utf-8
import base64
import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_bytes

from marketing import settings
from .forms import *


def base_context(request):
    context = {
        'signup_form': SignUpForm(request.POST),
        'login_form': AuthenticationForm(request.POST)
    }
    return context


def activate(request, url):
    data = json.loads(base64.b64decode(force_bytes(url)))
    user_id = data['user_id']
    user_confirmation = data['key']
    user = User.objects.get(pk=int(user_id))
    user.confirm_email(user_confirmation)
    if user.is_confirmed:
        user.is_active = True
        user.save()
        if user is not None:
            login(request, user)
        return redirect(reverse('main'))
    else:
        return HttpResponse('Link is invalid')


def confirm_transaction(request):
    if request.POST:
        transaction = TransactionKeys.objects.get(key_for_user=request.POST.get('transaction_key'))
        transaction.is_confirmed_by_user = True
        transaction.save()
        return JsonResponse(dict(success=True, message='Успешно подтвержено'))


def register_seven_admins(request):
    for i in range(7):
        user = User()
        user.email = "admin" + str(i) + "@localhost"
        user.username = "admin" + str(i)
        if settings.MOBILNIK:
            user.mobilnik = settings.MOBILNIK
        else:
            user.mobilnik = "123456789"
        if settings.ADMIN_PHONE:
            user.phone = settings.ADMIN_PHONE
        else:
            user.phone = "123456789"
        user.set_password(settings.DEFAULT_PASSWORD)
        user.save()
    return JsonResponse(dict(success=True, message='Все пользователи успешно зарегистрированы'))
