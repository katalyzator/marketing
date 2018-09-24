# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

import xlwt as xlwt
from dicttoxml import dicttoxml
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import *

from main.forms import *
from main.models import *
from django.utils.encoding import force_text
import json


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        context['products'] = Products.objects.all()
        context['users'] = User.objects.filter(is_active=True).distinct().count()
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
        # return JsonResponse(dict(success=False,message='Идут технические работы...'))
        if self.request.session['ref']:
            try:
                ref_user = User.objects.get(username=self.request.session['ref'])
            except:
                return JsonResponse(dict(success=False, message='Нет такого пользователя'))
        else:
            try:
                ref_user = User.objects.get(username=form.cleaned_data['sponsor'])
            except:
                return JsonResponse(dict(success=False, message='Нет такого пользователя'))
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
        context['transfer_form'] = TransferForm(self.request.POST)
        return context

    def form_valid(self, form):
        form.save()
        return JsonResponse(dict(success=True, message='Вы успешно изменили свои данные'))

    def form_invalid(self, form):
        message = ''
        for item in form.errors:
            message += form.errors[item]
        return JsonResponse(dict(succcess=False, message=message))


class TransactionCreateView(CreateView):
    model = TransactionKeys
    form_class = TransactionForm

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        if form.cleaned_data['product'].price <= int(self.request.user.points):
            form.save()
            return JsonResponse(dict(success=True, message='Вы успешно получили следующий уровень!'))
        return JsonResponse(dict(succes=False, message='У вас не хватает бонусов'))

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


class MarketingView(TemplateView):
    template_name = 'marketing-plan.html'


class PromoView(ListView):
    model = Products
    template_name = 'profile/personal-education.html'
    context_object_name = 'levels'

    def get_queryset(self):
        if self.request.user.level:
            return super(PromoView, self).get_queryset().filter(level__lte=self.request.user.level.level)
        return super(PromoView, self).get_queryset()


class SendPoints(CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'profile/personal-transactions.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.to_user = form.get_user()
        instance.save()
        return JsonResponse(
            dict(success=True, message=('Вы успешно передали %s бонусов' % (form.cleaned_data['amount']))))

    def form_invalid(self, form):
        message = ''
        print(form.errors)
        print(form.cleaned_data)
        for item in form.errors:
            message += form.errors[item]
        return JsonResponse(dict(succcess=False, message=message))


class ExportToXLS(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Users.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Пользователи')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Логин', 'Имя', 'Фамилия', 'Область', 'Город', 'Телефон', 'Email']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        rows = [(i.username, i.first_name, i.last_name, i.get_region_display(), i.city, i.phone, i.email)
                for i in
                User.objects.all()]
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response


class MobilnikResponse(View):
    def get(self, request):
        command = request.GET.get('command')
        account = request.GET.get('account')
        user_exists = User.objects.filter(wallet_id=account).exists()
        if command == 'check':
            if user_exists:
                user = User.objects.get(wallet_id=account)
                return HttpResponse(
                    dicttoxml({"result": 0, "first_name": str(user.first_name), "last_name": str(user.last_name)},
                              custom_root="response",
                              attr_type=False),
                    content_type='application/xhtml+xml')
            return HttpResponse(dicttoxml({"result": 1}, custom_root="response", attr_type=False),
                                content_type='application/xhtml+xml')
        elif command == 'pay':
            if user_exists:
                user = User.objects.get(wallet_id=account)
                txn_id = request.GET.get('txn_id')
                sum = request.GET.get('sum')
                Payments.objects.create(user=user, txn_id=txn_id, sum=sum)
                return HttpResponse(dicttoxml({"result": 0}, custom_root="response", attr_type=False),
                                    content_type='application/xml')
            return HttpResponse(dicttoxml({"result": 1}, custom_root="response", attr_type=False),
                                content_type='application/xml')
        return HttpResponse(status=400)


class TransactionsTemplateView(CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'profile/personal-transactions.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionsTemplateView, self).get_context_data(**kwargs)
        context['cash_request_form'] = CashRequestsForm(self.request.POST)
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super(TransactionsTemplateView, self).form_invalid(form)


class CashRequestsCreateView(CreateView):
    model = CashRequests
    form_class = CashRequestsForm
    template_name = 'profile/personal-transactions.html'

    def form_valid(self, form):
        if self.request.user.points > form.cleaned_data['points']:
            form.save()
            return JsonResponse(dict(success=True, message='Ваша заявка успешно оформлена'))
        return self.form_invalid(form)

    def form_invalid(self, form):
        message = ''
        if form.errors:
            for item in form.errors:
                message += form.errors[item]
            return JsonResponse(dict(succcess=False, message=message))
        return JsonResponse(dict(success=False, message='Недостаточно бонусов'))
