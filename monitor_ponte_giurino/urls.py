# from django.conf.urls import url
from django.urls import path
from monitor_ponte_giurino import views


urlpatterns = [
    path('', views.index, name='index'),
]