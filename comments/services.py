from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import PublicCommentForm

COMMENTS_PER_PAGE = 5           # Показывает количество комментариев, которые отображаются на странице (chunks)


def get_comments_context_data(parent_object, offset: int=0, request=None):
    """
    Сервисная функция для получения контекста блока комментариев.
    """

    all_comments_qs = Comment.objects.for_object(parent_object).filter(parent__isnull=True).active()
    content_type = ContentType.objects.get_for_model(parent_object)
    comment_form = PublicCommentForm()

    # Запрашиваем на один элемент больше, чем нужно для страницы.
    limit = COMMENTS_PER_PAGE + 1

    comments_with_extra = list(all_comments_qs[offset: offset + limit])

    has_more_comments = len(comments_with_extra) > COMMENTS_PER_PAGE

    comments_to_show = comments_with_extra[:COMMENTS_PER_PAGE]

    new_offset = offset + len(comments_to_show)

    total_comments_count = all_comments_qs.count()

    context = {
        'comments': comments_to_show,
        'comments_count': total_comments_count,
        'has_more_comments': has_more_comments,
        'new_offset': new_offset,

        'parent_object_id': parent_object.pk,
        'model_name': content_type.model,
        'content_type_id': content_type.id,

        'form': comment_form,
        'object': parent_object,
        'request': request,
    }

    return context