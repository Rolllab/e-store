from django.urls import path

from store.apps import StoreConfig
from store.views import index, ShopMainListView, ShopContactListView

app_name = StoreConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('shop/', ShopMainListView.as_view(), name='shop_main'),
    path('contact.html', ShopContactListView.as_view(), name='contact'),
]