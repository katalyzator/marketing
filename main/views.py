# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text
from django.views.generic import *
from django.contrib.auth.forms import PasswordChangeForm

from main.forms import *
from main.helpers import get_parent_user
from main.models import *


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        context['products'] = Products.objects.all()

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('ref'):
            request.session['ref'] = request.GET.get('ref')
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm

    def form_valid(self, form):
        ref_user = User.objects.get(username=self.request.session['ref'])
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активация аккаунта'
        message = render_to_string('partials/confirm_email.html', {
            'user': user,
            'domain': current_site.domain,
            'url': force_text(base64.b64encode(json.dumps({
                'user_id': user.pk,
                'key': user.confirmation_key
            }).encode()))
        })
        to_email = form.cleaned_data.get('email')
        try:
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        except:
            send_mail(mail_subject, message, 'wowtsty@gmail.com', [to_email], auth_password='124358911',
                      fail_silently=False)

        if ref_user:
            ref_user.related_users.add(user)
        return JsonResponse(dict(success=True, message='Вы успешно зарегистрированы, пожалуйста проверьте почту'))

    def form_invalid(self, form):
        message = ''
        for item in form.errors:
            message += form.errors.get(item)
        return JsonResponse(dict(success=False, message=message))


class UserLogoutView(LogoutView):
    template_name = 'index.html'

    def get_next_page(self):
        return reverse('main')


class UserLoginView(LoginView):
    template_name = 'base.html'

    def get_success_url(self):
        return reverse('main')


class UserDetailView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile/personal-area.html'

    def get_success_url(self):
        return self.request.path

    def get_template_names(self):
        if self.request.path == reverse('profile-settings'):
            return 'profile/personal-settings.html'
        if self.request.path == reverse('get_tariff'):
            return 'profile/personal-area-tarif.html'
        if self.request.path == reverse('profile-ref-urls'):
            return 'profile/personal-area-ref.html'
        if self.request.path == reverse('profile-requests'):
            return 'profile/personal-requests.html'
        return super(UserDetailView, self).get_template_names()

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        context['transaction_form'] = TransactionForm(self.request.POST)
        context['parent_user'] = get_parent_user(self.request.user, self.request.user)
        context['password_change_form'] = PasswordChangeForm(self.request.POST)
        context['user_requests'] = TransactionKeys.objects.filter(used_by=self.request.user, is_confirmed=False)
        return context

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(success=True, message='Вы успешно изменили свои данные'))

    def form_invalid(self, form):
        message = ''
        print(form.errors)
        for item in form.errors:
            message += form.errors[item]
        return JsonResponse(dict(succcess=False, message=message))


class TransactionCreateView(CreateView):
    model = TransactionKeys
    form_class = TransactionForm

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(success=True, message='Запрос успешно отправлен, ожидайте подтверждения от спонсора'))

    def form_invalid(self, form):
        message = ''
        for item in form.errors:
            message += form.errors.get(item)
        return JsonResponse(dict(succcess=False, message=message))


class UserPasswordChangeView(PasswordChangeView):
    title = 'Изменить пароль'

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(success=True, message='Вы успешно изменили свои данные'))

    def form_invalid(self, form):
        message = ''
        print(form.errors)
        for item in form.errors:
            message += form.errors[item]
        return JsonResponse(dict(succcess=False, message=message))
