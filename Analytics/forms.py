from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import SiteUser
from django.contrib.auth.models import Group


# Форма для создания нового пользователя
class SiteUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Используемая модель (SiteUser) и поля, которые будут отображаться в форме
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'group', 'is_staff', 'is_active')


# Форма для изменения данных пользователя
class SiteUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        # Используемая модель (SiteUser) и отображаемые поля
        model = SiteUser
        fields = ('username', 'email', 'group', 'is_staff', 'is_active')


# Форма для регистрации нового пользователя
class RegistrationForm(UserCreationForm):
    # Дополнительное поле для выбора группы из существующих
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Select Group')

    class Meta:
        # Используемая модель (SiteUser) и отображаемые поля в форме регистрации
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'group')


# Форма для входа пользователя в систему
class LoginForm(AuthenticationForm):
    class Meta:
        # Используемая модель (SiteUser) и отображаемые поля в форме входа
        model = SiteUser
        fields = ('username', 'password')