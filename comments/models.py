from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CommentQuerySet(models.QuerySet):
    """
    Кастомный QuerySet
    """
    def active(self):
        """Возвращает только активные комментарии."""
        return self.filter(active=True)


class CommentManager(models.Manager):
    """
    Кастомный менеджер, который использует мой QuerySet
    """
    def get_queryset(self):
        """Использую кастомный CommentQuerySet."""
        return CommentQuerySet(self.model, using=self._db)

    def for_object(self, obj):
        """
        Главный метод: получает QuerySet комментариев для указанного объекта.
        Это единая точка входа для получения комментариев.
        """

        content_type = ContentType.objects.get_for_model(obj)
        return self.get_queryset().filter(
            content_type=content_type,
            object_id=obj.pk
        ).order_by('-created', '-pk')                                   # Сразу сортируем по созданию и pk



class Comment(models.Model):
    """
    Общая модель комментариев. Может использоваться в любом приложении.
    """

    # Динамический блок (Формирует ForeignKey (и др.) динамически). Нужен для связки комментария и комментируемого объекта (Post, Product)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)         # ссылается на объект, который комментируется (класс модели — Post или Product)
    object_id = models.PositiveIntegerField()                                       # ID конкретного экземпляра объекта
    content_object = GenericForeignKey('content_type', 'object_id')   # связывает комментарий с объектом указанного класса и id

    # Статический блок
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # parent - это поле для ответов на комментарии
    #                               'self' — это поле связывает комментарий с другим комментарием (с самим собой)
    #                               null=True, blank=True — обязательно, так как у комментариев верхнего уровня родителя нет
    #                               related_name='replies' — это то, что позволяет в шаблоне делать comment.replies.all.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # Создаем экземпляр custom-менеджера
    objects = CommentManager()

    class Meta:
        ordering = ['-created']                              # Для сортировки комментариев обратном порядке
        indexes = [                                          # Для индексирования поля created в возрастающем порядке
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.name


    def get_replies(self):
        """Получает все ответы на данный комментарий."""
        return self.replies.all()

