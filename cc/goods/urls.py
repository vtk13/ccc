from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^goods/list$', views.goods_list, name='goods_list'),
    url(r'^goods/view/(?P<good_id>[0-9]+)$', views.goods_view, name='goods_view'),
    url(r'^goods/add$', views.GoodAdd.as_view(), name='good_add'),
    url(r'^goods/edit/(?P<id>[0-9]+)$', views.GoodEdit.as_view(), name='good_edit'),
    url(r'^shops/list$', views.shops_list, name='shops_list'),
    url(r'^shops/add$', views.ShopAdd.as_view(), name='shop_add'),
    url(r'^sales/list$', views.sales_list, name='sales_list'),
    url(r'^sales/add$', views.CostAdd.as_view(), name='sale_add'),
    url(r'^ajax/goods/(?P<query>.*)$', views.ajax_goods, name='ajax_goods'),
    url(r'^ajax/shops/(?P<query>.*)$', views.ajax_shops, name='ajax_shops'),
]
