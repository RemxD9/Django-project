from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SiteUser
from django.contrib.auth.models import Group


class RegistrationForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Select Group')

    class Meta:
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'group')


class LoginForm(AuthenticationForm):
    class Meta:
        model = SiteUser
        fields = ('username', 'password')
