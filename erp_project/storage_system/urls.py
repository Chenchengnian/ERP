from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = 'storage_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^custom_list$', views.custom_list, name='custom_list'),
    url(r'^create_custom$', views.create_custom, name='create_custom'),
    url(r'^custom_search/$', views.custom_search, name='custom_search'),
    url(r'^product_list$', views.product_list, name='product_list'),
    url(r'^product_sold_list', views.product_sold_list, name='product_sold_list'),
    url(r'^create_product$', views.create_product, name='create_product'),
    url(r'^product_search/$', views.product_search, name='product_search'),
    url(r'^sold_project', views.sold_project, name='sold_project'),
    url(r'^product_detail/(?P<pid>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^product_update/(?P<pid>\d+)/$', views.product_update, name='product_update')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
