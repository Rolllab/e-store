from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Comment


class PublicCommentForm(forms.ModelForm):
    """
    Форма для публичного сайта
    """

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'reviews__comment--reply__input',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'reviews__comment--reply__input',
                'placeholder': 'Ваша почта'
            }),
            'body': forms.Textarea(attrs={
                'class': 'reviews__comment--reply__textarea',
                'placeholder': 'Введите комментарий'
            })
        }


class ReplyCommentForm(forms.ModelForm):
    """
    Упрощенная форма для ОТВЕТОВ на комментарии.
    Включает ТОЛЬКО поле для текста.
    """
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'reviews__comment--reply__textarea',
                'placeholder': 'Ваш ответ...',
                'rows': 3
            })
        }



class AdminCommentForm(forms.ModelForm):
    """
    Форма для админки.
    Используется при создании комментария (в общих комментариях) в админке и для выбора приложения (app) из выпадающего списка.
    """

    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        label='Тип объекта',
        help_text='Выберите тип объекта, к которому относится комментарий.'
    )
    object_id = forms.IntegerField(
        label='ID объекта',
        help_text='Введите ID объекта, к которому относится комментарий.'
    )

    class Meta:
        model = Comment
        fields = ['content_type', 'object_id', 'name', 'email', 'body', 'active']


    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        object_id = cleaned_data.get('object_id')

        if content_type and object_id:
            try:
                content_type.get_object_for_this_type(id=object_id)
            except content_type.model_class().DoesNotExist:
                raise forms.ValidationError('Объект с указанным типом и ID не найден.')

        return cleaned_data