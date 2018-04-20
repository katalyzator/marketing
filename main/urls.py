from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from main.helpers import *
from main.views import *

urlpatterns = [
    url(r'^$', SliderListView.as_view(), name='main'),
    url(r'^create_user/$', UserCreateView.as_view(), name='create_user'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    url(r'^profile/$', login_required(UserDetailView.as_view()), name='profile'),
    url(r'^profile/settings/$', login_required(UserDetailView.as_view()), name='profile-settings'),
    url(r'^profile/tarif/$', login_required(UserDetailView.as_view()), name='get_tariff'),
    url(r'^activate/(?P<url>.*)$', activate, name='activate'),
]
