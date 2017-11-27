"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from development.views import index, SignUp, login_view, propertyx, logout_view, forget_password, password_reset_form, password_reset_complete, password_reset_confirm
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.conf.urls.static import static
from development import views
from development.router import router
from rest_framework import routers, serializers, viewsets


login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')
logout_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^list/$', views.list_all, name='list'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^export_all/(?P<type>[a-zA-Z]+)/$', views.export_xlsx_all, name='export_all'),
    #url(r'^search/(?:search=(?P<search_data>[a-zA-Z]+))/$', views.search, name='search'),
    #url(r'^our_property/(?P<idx>[0-9\-1]+)', property, name='property'),
    url(r'^our_property/$', propertyx, name='property'),
    url(r'^$', views.about, name='main'),
    url(r'^login/$', login_forbidden(login_view), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', SignUp, name='register'),
    url(r'^forget_password/$', forget_password, name='forget_password'),
    url(r'^password_reset/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_form, name='password_reset'),
    url(r'^password_reset_complete/$', password_reset_complete, name='password_reset_complete'),
    url(r'^password_reset_sent/$', password_reset_confirm, name='password_reset_sent'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/password_validation/$', views.password_validation, name='password_validation'),
    url(r'^ajax/get_all/$', views.get_all, name='get_all'),
    url(r'^ajax/active/$', views.active, name='active'),
    url(r'^ajax/postponed/$', views.postponed, name='postponed'),
    url(r'^ajax/cancelled/$', views.cancelled, name='cancelled'),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'townauction/update-partial/(?P<pk>\d+)/$', views.TownAuctionView.as_view()),
    url(r'baystateauction/update-partial/(?P<pk>\d+)/$', views.BayStateAuctionView.as_view(), name='baystateauction'),
    url(r'timeline', views.TimelineView.as_view(), name='timeline'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
