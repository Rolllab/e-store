from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from store.models import Product


def index(request):
    context = {
        'title': 'Furea - Furniture eCommerce'
    }
    return render(request, 'store/index.html', context=context)

# def index(request):
#     context = {
#         'object_list': Batch.allocate()
#         'title': 'Питомник - Главная'
#     }
#     return render(request, 'dogs/index.html', context)

# def shop(request):
#     return render(request, 'store/shop.html')

class ShopMainListView(ListView):
    model = Product
    template_name = 'store/shop.html'
    extra_context = {
        'title': 'Мой первый title'
    }

class ShopContactListView(TemplateView):
    template_name = 'store/contact.html'
