from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    paginate_by = 3

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

    def paginate_queryset(self, queryset, page_size):
        """
        Переопределяем пагинацию:
        - При PageNotAnInteger (не число) → первая страница.
        - При EmptyPage (страницы не существует) → последняя страница.
        """
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get('page', 1)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # Если page не число (например, ?page=abc) → показываем первую страницу
            page_obj = paginator.page(1)
        except EmptyPage:
            # Если страницы не существует (например, ?page=999) → показываем последнюю
            page_obj = paginator.page(paginator.num_pages)

        return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()


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
