"""cross_token URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-panel/', views.admin, name='admin-panel'),
    path('alice/', views.alice, name='alice'),
    path('bob/', views.bob, name='bob'),

    path('init-eth/', views.init_eth, name='init_eth'),
    path('init-bsc/', views.init_bsc, name='init_bsc'),
    path('transfer-eth/', views.transfer_eth, name='transfer_eth'),
    path('transfer-bsc/', views.transfer_bsc, name='transfer_bsc'),

    path('alice-burn/', views.alice_burn, name='alice_burn'),

    path('admin/', admin.site.urls),
]