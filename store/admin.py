from django.contrib import admin
from .models import Product, Bed, Sofa

# Базовый класс админки для Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')         # Поля, отображаемые в списке
    list_filter = ('is_available',)                          # Фильтры
    search_fields = ('name', 'description')                  # Поля для поиска

# Класс админки для Bed
class BedAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'size', 'material', 'is_available')
    list_filter = ('is_available', 'material')
    search_fields = ('name', 'description', 'size')

# Класс админки для Sofa
class SofaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_folding', 'upholstery', 'is_available')
    list_filter = ('is_available', 'is_folding', 'upholstery')
    search_fields = ('name', 'description', 'upholstery')


# Регистрация моделей с custom-админ-классами
admin.site.register(Product, ProductAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Sofa, SofaAdmin)
