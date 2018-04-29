# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.views.generic import *

from main.forms import *
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
        else:
            request.session['ref'] = None
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm

    def form_valid(self, form):
        if self.request.session['ref']:
            ref_user = User.objects.get(username=self.request.session['ref'])
        else:
            ref_user = User.objects.get(username=form.cleaned_data['sponsor'])
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
        print(form.errors)
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

    def form_valid(self, form):
        login(self.request, form.get_user())
        return JsonResponse(dict(success=True, message='Успешно'))

    def form_invalid(self, form):
        message = ''
        for item in form.errors:
            message += form.errors.get(item)
        return JsonResponse(dict(sucess=False, message=message))


class UserDetailView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profile/personal-area.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('main'))
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)

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
        current_site = get_current_site(self.request)
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['domain'] = current_site.domain
        context['products'] = Products.objects.order_by('level')
        context['transaction_form'] = TransactionForm(self.request.POST)
        context['password_change_form'] = PasswordChangeForm(self.request.POST)
        context['user_requests'] = TransactionKeys.objects.filter(used_by=self.request.user, is_confirmed_by_user=False)
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

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse('main'))
        return super(UserPasswordChangeView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('main')

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(success=True, message='Вы успешно изменили свои данные'))

    def form_invalid(self, form):
        message = ''
        print(form.errors)
        for item in form.errors:
            message += form.errors[item]
        return JsonResponse(dict(succcess=False, message=message))


class ReferalsListView(DetailView):
    model = User
    template_name = 'profile/personal-referals.html'

    def get_object(self, queryset=None):
        return self.request.user


class SponsorsLitView(DetailView):
    model = User
    template_name = 'profile/personal-area-sponsor.html'

    def get_object(self, queryset=None):
        return self.request.user


class AgreementDetailView(DetailView):
    model = Agree
    context_object_name = 'agree'
    template_name = 'agreement.html'

    def get_object(self, queryset=None):
        return Agree.objects.first()


class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('main'))  # or http response
        return None
