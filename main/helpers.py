# coding=utf-8
import base64
import json

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_bytes

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


def get_parent_user(user, real_user):
    try:
        parent_user = User.objects.get(level__gt=user.level.level, related_users=user)
        if parent_user and TransactionKeys.objects.filter(handler=real_user, used_by=parent_user,
                                                          is_confirmed=True).first():
            return get_parent_user(parent_user, real_user)
        return parent_user
    except:
        parent_user = User.objects.filter(level__gte=user.level.level, related_users=user).order_by(
            'level__level').last()
        if parent_user and TransactionKeys.objects.filter(handler=real_user, used_by=parent_user, is_confirmed=True).first():
            return get_parent_user(parent_user, real_user)
        return parent_user


def confirm_transaction(request):
    if request.POST:
        transaction = TransactionKeys.objects.get(key=request.POST.get('transaction_key'))
        transaction.is_confirmed = True
        transaction.save()
        return JsonResponse(dict(success=True, message='Успешно подтвержено'))
