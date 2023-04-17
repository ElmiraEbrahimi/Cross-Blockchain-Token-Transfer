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
from django.views.decorators.csrf import csrf_exempt

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('owner/', views.owner, name='owner'),
    path('alice/', views.alice, name='alice'),
    path('bob/', views.bob, name='bob'),

    path('compile_contract/', views.compile_contract, name='compile_contract'),
    path('deploy_eth/', views.deploy_eth, name='deploy_eth'),
    path('deploy_bsc/', views.deploy_bsc, name='deploy_bsc'),

    path('init-eth/', views.init_eth, name='init_eth'),
    path('init-bsc/', views.init_bsc, name='init_bsc'),
    path('transfer-eth/', views.transfer_eth, name='transfer_eth'),
    path('transfer-bsc/', views.transfer_bsc, name='transfer_bsc'),

    path('alice-burn/', views.alice_burn, name='alice_burn'),

    path('set_event_handler_status_true/', views.set_event_handler_status_true, name='set_event_handler_status_true'),
    path('get_w3_and_contract_addresses/', views.get_w3_and_contract_addresses, name='get_w3_and_contract_addresses'),
    path('submit_event/', csrf_exempt(views.submit_event), name='submit_event'),

    path('admin/', admin.site.urls, name='admin'),
]
