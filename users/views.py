import random
import string

from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:user_login')
    template_name = 'users/user-login-registration.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['flag'] = True
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        send_register_email(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/user-login-registration.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Вход в аккаунт'
    }

    def get_success_url(self):
        # Проверяем, что пользователь аутентифицирован
        if self.request.user.is_authenticated:
            return reverse_lazy('users:users_detail', kwargs={'pk': self.request.user.pk})
        return reverse_lazy('users:user_login')  # fallback, если что-то пошло не так


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_profile_read_only.html'
    extra_context = {
        'title': 'Ваш профиль'
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = dict(title='Изменить профиль')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/user_change_password.html'
    success_url = reverse_lazy('users:user_profile')
    extra_context = {
        'title': 'Изменить пароль'
    }


class UserLogoutView(LogoutView):                               # My class
    # template_name = 'users/user_login.html'
    # extra_context = {
    #     'title': 'Вход в аккаунт'
    # }
    pass


class UserListView(LoginRequiredMixin, ListView):
    model = User
    extra_context = {
        'title': 'Питомник... Здесь собраны все наши пользователи'
    }
    template_name = 'users/users.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-account.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        user_obj = self.get_object()
        context_data['title'] = f'Профиль пользователя {user_obj}'
        context_data['object'] = user_obj
        return context_data


@login_required
def user_generate_new_password_view(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


class UserPersonalDataView(ListView):                       # My class
    model = User
    template_name = 'users/user-personal-data.html'
    extra_context = {
        'title': 'Персональные данные'
    }
