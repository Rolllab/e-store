from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()             # Используем только опубликованные посты
    context_object_name = 'posts'               # В шаблоне будет - {% for post in posts %} (список постов).
    template_name = 'blog/blog.html'
    extra_context = {
        'title': 'Блог'
    }


# def post_list(request):                       # удалить, если BlogListView написан корректно
#     posts = Post.published.all()
#     return render(
#         request=request,
#         template_name='blog/post/list.html',
#         context={'posts': posts}
#     )


class PostDetailView(DetailView):
    queryset = Post.published.all()             # Используем только опубликованные посты
    template_name = 'blog/blog-detail.html'
    context_object_name = 'post'                # Имя переменной в шаблоне (необязательно, но желательно)
    extra_context = {
        'title': 'Пост'
    }


# def post_detail(request, id):                   # удалить, если PostDetailView написан корректно
#     post = get_object_or_404(
#         Post,
#         id=id,
#         status=Post.Status.PUBLISHED
#     )
#     return render(
#         request,
#         'blog/post/detail.html',
#         {'post': post}
#         )
