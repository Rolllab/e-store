from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Q

from .models import Comment
from .forms import AdminCommentForm


class CommentInline(GenericTabularInline):
    """
    Только для inline комментариев (идут вместе с постом)
    """
    model = Comment
    fields = ('name', 'email', 'body', 'active')                # Поля для отображения
    extra = 0                                                   # Количество пустых форм для добавления
    readonly_fields = ('created', 'updated')                    # Даты лучше сделать только для чтения


class ObjectTypeFilter(admin.SimpleListFilter):
    """
    Вспомогательный класс для фильтрации content_object (в models.py). Используется в CommentAdmin.
    """
    title = 'Тип объекта'
    parameter_name = 'object_type'

    def lookups(self, request, model_admin):
        types = set([obj.content_type for obj in Comment.objects.all()])
        return [(ct.pk, ct.model_class().__name__) for ct in types]

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        return queryset.filter(content_type__id=value)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Для общих комментариев со всех приложений (ограниченных get_form())
    """
    form = AdminCommentForm
    list_display = ('name', 'email', 'content_object', 'created', 'active')
    list_filter = (ObjectTypeFilter, 'active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    # readonly_fields = ['content_object']

    def get_form(self, request, obj=None, **kwargs):
        # Получаем форму
        form = super().get_form(request, obj, **kwargs)

        # Создаем фильтр для нужных нам моделей.
        # Указываем здесь нужные app_label и model (для каждого нужного приложения) в нижнем регистре
        q_filter = (Q(app_label='blog', model='post') |
                    Q(app_label='store', model='product'))

        # Применяем фильтр к queryset поля content_type
        form.base_fields['content_type'].queryset = ContentType.objects.filter(q_filter)

        return form
