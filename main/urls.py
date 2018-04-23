from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from main.helpers import *
from main.views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='main'),
    url(r'^create_user/$', UserCreateView.as_view(), name='create_user'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    url(r'^profile/$', login_required(UserDetailView.as_view()), name='profile'),
    url(r'^profile/settings/$', login_required(UserDetailView.as_view()), name='profile-settings'),
    url(r'^profile/tarif/$', login_required(UserDetailView.as_view()), name='get_tariff'),
    url(r'^profile/ref/$', login_required(UserDetailView.as_view()), name='profile-ref-urls'),
    url(r'^profile/requests/$', login_required(UserDetailView.as_view()), name='profile-requests'),
    url(r'^transaction/$', login_required(TransactionCreateView.as_view()), name='transaction'),
    url(r'^transaction/confirm/$', login_required(confirm_transaction), name='confirm-transaction'),
    url(r'^change_password/$', login_required(UserPasswordChangeView.as_view()), name='change_password'),
    url(r'^activate/(?P<url>.*)$', activate, name='activate'),
    url(r'^agree/$', aggreement_view, name='aggre_view')
]
