from django.conf.urls import url

from main.helpers import *
from main.views import *

urlpatterns = [
    url(r'^$', SliderListView.as_view(), name='main'),
    url(r'^create_user/$', UserCreateView.as_view(), name='create_user'),
    url(r'^activate/(?P<url>.*)$', activate, name='activate'),
]
