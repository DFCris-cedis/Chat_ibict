from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import CustomUser
from django import forms
from .models import Test
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


class MeuForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['phraseTest']

    # phraseTest = forms.CharField(label='Digite aqui seu texto:')
    phraseTest = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': 'Digite aqui seu texto'}))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Endereço de e-mail',
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control'}),
        max_length=254,
    )
