# coding=utf-8
import base64
import json
import random
import string

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes

from marketing import settings
from .forms import *


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def base_context(request):
    context = {
        'signup_form': SignUpForm(request.POST),
        'login_form': AuthenticationForm(request.POST)
    }
    return context


def activate(request, url):
    try:
        data = json.loads(base64.b64decode(force_bytes(url)))
    except:
        data = json.loads(base64.b64decode(force_bytes(url + '==')))
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


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('reset_email')
        try:
            user = User.objects.get(email=email)
            to_email = email
            password = id_generator()
            user.set_password(password)
            update_session_auth_hash(request, user)
            user.save()
            try:
                mail_subject = 'Восстановление пароля'
                message = render_to_string('partials/reset_password.html', {
                    'user': user,
                    'password': password
                })
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            except:
                mail_subject = 'Восстановление пароля'
                message = render_to_string('partials/reset_password.html', {
                    'user': user,
                    'password': password
                })

                send_mail(mail_subject, message, 'wowtsty@gmail.com', [to_email], auth_password='124358911',
                          fail_silently=False)
            return JsonResponse(
                dict(success=True, message='Мы отправили на ваше имейл, письмо. Пожалуйста прочтите его!'))
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message='Такой Email не используется нашими пользователями'))
    else:
        return JsonResponse(dict(success=False, message='Это не пост запрос'))
