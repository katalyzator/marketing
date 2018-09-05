from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from main.helpers import page_not_found
from marketing import settings

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),
    # url(r'', include('main.urls'))
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
if not settings.ON_WORK:
    urlpatterns.append(url(r'', include('main.urls')))
else:
    urlpatterns.append(url(r'', page_not_found, name='error'))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
