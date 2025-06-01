from django.views.generic import ListView
from django.shortcuts import render
from store.models import Product


def index(request):
    return render(request, 'store/index.html')

# def index(request):
#     context = {
#         'object_list': Batch.allocate()
#         'title': 'Питомник - Главная'
#     }
#     return render(request, 'dogs/index.html', context)

def shop(request):
    return render(request, 'store/shop.html')

class ShopMainListView(ListView):
    model = Product
    template_name = 'store/shop.html'
    extra_context = {
        'title': 'Мой первый title'
    }

