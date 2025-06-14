from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from blog.models import Post


class PostListView(ListView):
    """
    Для отображения списка постов в блоге.
    """
    queryset = Post.published.all()             # Используем только опубликованные посты
    context_object_name = 'posts'               # В шаблоне будет - {% for post in posts %} (список постов).
    template_name = 'blog/blog.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """
        Это один из вариантов extra_context.
        Так можно передать множество параметров. Этот метод более гибкий, чем extra_content

        :param kwargs:
        :return: values
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


# def post_list(request):                       # удалить, если BlogListView написан корректно
#     post_list_ = Post.published.all()
#     # Постраничная разбивка с 3 постами на страницу
#     paginator = Paginator(post_list_, 3)
#     page_number = request.GET.get('page', 1)
#     posts = paginator.page(page_number)
#     return render(
#         request,
#         'blog/post/list.html',
#         {'posts': posts}
#     )


class PostDetailView(DetailView):
    queryset = Post.published.all()             # Используем только опубликованные посты
    template_name = 'blog/blog-detail.html'
    context_object_name = 'post'                # Имя переменной в шаблоне (необязательно, но желательно)
    extra_context = {
        'title': 'Пост'
    }

    def get_object(self, queryset=None):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['post']

        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=slug,
            publish__year=year,
            publish__month=month,
            publish__day=day
        )


# def post_detail(request, year, month, day, post):                   # удалить, если PostDetailView написан корректно
#     post = get_object_or_404(
#         Post,
#         status=Post.Status.PUBLISHED,
#         slug=post,
#         publish__year=year,
#         publish__month=month,
#         publish__day=day
#     )
#     return render(
#         request,
#         'blog/post/detail.html',
#         {'post': post}
#     )
