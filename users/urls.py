from django.urls import path

from users.apps import UsersConfig
from users.views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView, UserUpdateView, \
    UserPasswordChangeView, user_generate_new_password_view, UserListView, UserDetailView, UserPersonalDataView

app_name = UsersConfig.name

urlpatterns = [
    # Работа с аккаунтом
    path('login/', UserLoginView.as_view(), name='user_login'),
    # path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change_password/', UserPasswordChangeView.as_view(), name='user_change_password'),
    path('profile/genpassword/', user_generate_new_password_view, name='user_generate_new_password'),

    # Просмотр пользователей
    path('all_users/', UserListView.as_view(), name='users_list'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<int:pk>/personal-data/', UserPersonalDataView.as_view(), name='user_personal_data'),

]