from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Эл. почта')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='Anonym')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)             # не обязательное поле
    telegram = models.CharField(max_length=150, verbose_name='Телеграм', **NULLABLE)        # не обязательное поле
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)       # не обязательное поле
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

