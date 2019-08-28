from django.conf.urls import url

from . import views

app_name = 'storage_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^custom_list$', views.custom_list, name='custom_list'),
    url(r'^create_custom$', views.create_custom, name='create_custom'),
    url(r'^custom_search/$', views.custom_search, name='custom_search'),
    url(r'^product_list$', views.product_list, name='product_list'),
    url(r'^product_sold$', views.product_sold, name='product_sold'),
    url(r'^create_product$', views.create_product, name='create_product'),
]
