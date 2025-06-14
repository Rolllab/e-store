from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
# from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password

from users.models import User
# from users.validators import validate_password


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        # fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')    # Один из вариантов записи
        exclude = ('is_active', )                                             # Другой вариант записи


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    # Версия gpt
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #
    #     if password1 != password2:
    #         raise ValidationError("Пароли не совпадают!")
    #
    #     try:
    #         validate_password(password2, self.user)  # Стандартные проверки
    #     except ValidationError as e:
    #         raise ValidationError(e.messages)
    #
    #     return password2

    def clean_password2(self):
        cd = self.cleaned_data
        validate_password(cd['password1'])
        if cd['password1'] != cd['password2']:
            print('Пароли не совпадают!!!')
            raise forms.ValidationError('Пароли не совпадают !!!')
        return cd['password2']


class UserLoginForm(AuthenticationForm):
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        validate_password(password1)
        if password1 and password2 and (password1 != password2):
            raise ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')
        validate_password(password2, self.user)
        return password2
