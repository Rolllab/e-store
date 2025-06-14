from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']                                   # Отдельная строка поиска
    prepopulated_fields = {'slug': ('title',)}                          # Предварительно заполненное поле slug (slug=title)
    raw_id_fields = ['author']                                          # Заменяет выпадающий список поисковым ВИДЖЕТОМ,
    date_hierarchy = 'publish'                                          # Навигация по иерархии дат
    ordering = ['status', 'publish']                                    # Критерии сортировки по умолчанию
    # show_facets = admin.ShowFacets.ALWAYS                               # Всегда показывает счетчики
