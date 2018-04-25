from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from marketing import settings

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('main.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
