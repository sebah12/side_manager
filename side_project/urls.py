"""side_project URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from manager import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^manager/', views.manager, name='manager'),
    url(r'^marcas/(?P<pk>\d+)/$', views.marca, name='marca'),
    url(r'^marcas/new/$', views.new_marca, name='new_marca'),
    url(r'^marcas/', views.marcas, name='marcas'),
    url(r'^productos/new/$', views.new_item, name='new_item'),
    url(r'^productos/', views.productos, name='productos'),
    url(r'^admin/', admin.site.urls),
]
