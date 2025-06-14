from django.conf import settings
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    """
    Это конкретно-прикладной модельный менеджер. Он позволяет извлекать посты, имеющие статус PUBLISHED.
    """
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'                   # Статус - Черновик
        PUBLISHED = 'PB', 'Published'           # Статус - Опубликован


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    objects = models.Manager()          # менеджер, применяемый по умолчанию
    published = PublishedManager()      # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish']         # Посты будут возвращаться в обратном хронологическом порядке
        indexes = [                     # Добавление индекса базы данных
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
