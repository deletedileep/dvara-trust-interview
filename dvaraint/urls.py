from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.conf.urls import url, include

from dvaraint import settings
from django.conf.urls.static import static
from public import views

urlpatterns = [
    url(r'^', include('public.urls')),
    url(r'^super_admin/', admin.site.urls),
    url(r'^admin_portal/', include('admin_portal.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<slug>[a-z0-9-_]+)/$', views.dynamic_page, name='dynamic_page'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
