from django.urls import path

from .views import (CommentsView, CommentCreateView, LoadCommentsView, CommentReplyFormView, CommentCountView,
                    CommentReplyCountView, CommentRepliesView)


app_name = 'comments'

# model_name                - имя модели, например "post" или "product"
# object_id                 - PK родительского объекта

urlpatterns = [
    path('<str:model_name>/<int:object_id>/comment/', CommentsView.as_view(), name='post_comment'),
    path('<str:model_name>/<int:object_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('load-more/<str:model_name>/<int:object_id>/', LoadCommentsView.as_view(), name='load_more_comments'),
    path('reply-form/<int:parent_id>/', CommentReplyFormView.as_view(), name='get_reply_form'),
    path('count/<int:content_type_id>/<int:object_id>/', CommentCountView.as_view(), name='comment-count'),
    path('reply-count/<int:content_type_id>/<int:object_id>/<int:comment_id>/', CommentReplyCountView.as_view(), name='comment-reply-count'),
    path('toggle-replies/<int:comment_id>/', CommentRepliesView.as_view(), name='comment_replies'),
]
