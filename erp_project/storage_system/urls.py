from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = 'storage_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^custom_list/$', views.custom_list, name='custom_list'),
    url(r'^create_custom/$', views.create_custom, name='create_custom'),
    url(r'^custom_update/(?P<cid>\d+)/$', views.custom_update, name='custom_update'),
    url(r'^custom_search/$', views.custom_search, name='custom_search'),
    url(r'^product_list/$', views.product_list, name='product_list'),
    url(r'^product_sold_list/$', views.product_sold_list, name='product_sold_list'),
    # url(r'^sold_product_search/$', views.sold_product_search, name='sold_product_search'),
    url(r'^today_sold_list/$', views.today_sold_list, name='today_sold_list'),
    url(r'^month_sold_list/$', views.month_sold_list, name='month_sold_list'),
    url(r'^product_category_list/(?P<cid>\d+)/$', views.product_category_list, name='product_category_list'),
    url(r'^product_custom_list/(?P<cid>\d+)/$', views.product_custom_list, name='product_custom_list'),
    url(r'^create_product/$', views.create_product, name='create_product'),
    url(r'^product_search/$', views.product_search, name='product_search'),
    url(r'^product_sold/(?P<pid>\d+)/$', views.product_sold, name='product_sold'),
    url(r'^product_detail/(?P<pid>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^product_update/(?P<pid>\d+)/$', views.product_update, name='product_update'),
    url(r'^sold_product_update/(?P<pid>\d+)/$', views.sold_product_update, name='sold_product_update'),
    url(r'^sold_product_delete/(?P<pid>\d+)/$', views.sold_product_delete, name='sold_product_delete'),
    url(r'^create_category/$', views.create_category, name='create_category'),
    url(r'^category_list/$', views.category_list, name='category_list'),
    url(r'^category_update/(?P<cid>\d+)/$', views.category_update, name='category_update'),
    url(r'^total_data/$', views.total_data, name='total_data'),
    url(r'^sale_data_by_day/$', views.sale_data_by_day, name='sale_data_by_day'),
    url(r'^sale_data_by_month/$', views.sale_data_by_month, name='sale_data_by_month'),
    url(r'^sale_data_by_year/$', views.sale_data_by_day, name='sale_data_by_year'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
