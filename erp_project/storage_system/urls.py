from django.conf.urls import url

from . import views

app_name = 'storage_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
]
