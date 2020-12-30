"""tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path, include
from rango import views
from rango.views import MyRegistrationView
import re


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^about/', views.hello, name='about'),
    re_path(r'add_category/$', views.add_category, name='add_category'),
    re_path(r'category/(?P<category_name_url>\w+)/$', views.category, name='category'),
    #re_path(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    re_path(r'register/$', views.register, name='register'),
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'restricted/', views.restricted, name='restricted'),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    re_path(r'^accounts/',include('registration.backends.simple.urls')),
    re_path(r'^accounts/register/$',MyRegistrationView.as_view(), name='registration_register'),
    re_path(r'search/$', views.search, name='search'),
    re_path(r'^like/$', views.like_category, name='like_category'),
    re_path(r'^suggest/$', views.suggest_category, name='suggest_category'),
    re_path(r'ˆadd/$', views.auto_add_page, name='auto_add_page'),
    ]
