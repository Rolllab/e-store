from django import template
from comments.services import get_comments_context_data

register = template.Library()


@register.inclusion_tag('comments/partials/_comments_block.html', takes_context=True)
def render_comments_for_object(context, obj):
    """
    Отображает начальный блок комментариев для объекта.
    """

    return get_comments_context_data(parent_object=obj, offset=0)