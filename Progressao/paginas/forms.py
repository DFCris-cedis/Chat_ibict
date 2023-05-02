from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Test



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

from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new_password', 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new_password', 'class': 'form-control'}),
    )
