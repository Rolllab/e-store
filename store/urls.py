from django.urls import path
from store.views import index, ShopMainListView

urlpatterns = [
    path('', index, name='index'),
    path('shop.html', ShopMainListView.as_view(), name='shop'),
]