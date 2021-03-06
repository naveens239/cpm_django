"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import cpm.views


urlpatterns = [
    url(r'^$', cpm.views.home, name='home'),
    url(r'^contact/$', cpm.views.contact, name='contact'),
    url(r'^about/$', cpm.views.about, name='about'),
    url(r'^profile/$', cpm.views.profile, name='profile'),
    url(r'^addproject/$', cpm.views.addproject, name='addproject'),
    url(r'^netproject/$', cpm.views.netproject, name='netproject'),
    url(r'^projectoverview/(?P<name>.*)/$', cpm.views.projectoverview, name='projectoverview'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^projectsettings/(?P<name>.*)/$', cpm.views.projectsettings, name='projectsettings'),
    url(r'^projectdetails/(?P<name>.*)/$', cpm.views.projectdetails, name='projectdetails'),
    url(r'^get_category/$', cpm.views.get_category, name='get_category'),
    url(r'^get_sub_category/(?P<category>.*)/$', cpm.views.get_sub_category, name='get_sub_category'),
    url(r'^get_vendors/$', cpm.views.get_vendors, name='get_vendors'),
    url(r'^register_vendor/$', cpm.views.register_vendor,name='register_vendor'),
    url(r'^api/', include('api.urls')),
]+static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
	 urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	 urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)