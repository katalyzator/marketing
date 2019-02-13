from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from main.helpers import *
from main.mobilnik import MobilnikPayEvent, mobilnik_response
from main.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='main'),
    url(r'^create_user/$', UserCreateView.as_view(), name='create_user'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    url(r'^profile/$', login_required(UserDetailView.as_view(), login_url='/'), name='profile'),
    url(r'^profile/settings/$', login_required(UserDetailView.as_view(), login_url='/'), name='profile-settings'),
    url(r'^profile/tarif/$', login_required(UserDetailView.as_view(), login_url='/'), name='get_tariff'),
    url(r'^profile/ref/$', login_required(UserDetailView.as_view(), login_url='/'), name='profile-ref-urls'),
    url(r'^profile/referals/$', login_required(ReferalsListView.as_view(), login_url='/'), name='profile-referals'),
    url(r'^profile/sponsors/$', login_required(SponsorsLitView.as_view(), login_url='/'), name='profile-sponsors'),
    url(r'^profile/transactions/$', login_required(TransactionsTemplateView.as_view(), login_url='/'),
        name='profile-transactions'),
    url(r'^profile/education/$', login_required(PromoView.as_view(), login_url='/'),
        name='profile-education'),
    url(r'^transaction/$', login_required(TransactionCreateView.as_view(), login_url='/'), name='transaction'),
    url(r'^change_password/$', login_required(UserPasswordChangeView.as_view(), login_url='/'),
        name='change_password'),
    url(r'^activate/(?P<url>.*)$', activate, name='activate'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^agree/$', AgreementDetailView.as_view(), name='agreement'),
    url(r'^set_admin/$', register_seven_admins, name='set_admin'),
    url(r'^marketing/$', MarketingView.as_view(), name='mark_view'),
    url(r'^news/(?P<slug>[\w-]+)/$', NewsDetailView.as_view(), name='news-detail'),
    url(r'^send_points/$', SendPoints.as_view(), name='send_points'),
    url(r'^mobilnik/$', MobilnikPayEvent.as_view(), name='mobilnik'),
    url(r'^mobilnik/terminal/response/$', MobilnikResponse.as_view(), name='mobilnik-terminal'),
    url(r'^asisnur/terminal/response/$', AsisNurResponse.as_view(), name='asisnur-terminal'),
    url(r'^export_to_xls/$', ExportToXLS.as_view(), name='export_to_xls'),
    url(r'^cash-request/$', CashRequestsCreateView.as_view(), name='cash_request'),
    url(r'^mobilnik/response/$', mobilnik_response, name='mobilnik-response'),
]
handler404 = 'myapp.helpers.page_not_found'
