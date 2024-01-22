from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django import forms
from .models import Test



class MeuForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['phraseTest', 'title']

    # phraseTest = forms.CharField(label='Digite aqui seu texto:')
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'title', 'placeholder': 'Digite seu título...'}
        )
    )    

    phraseTest = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'textarea', 'placeholder': 'Digite aqui seu texto. (O texto precisa conter no mínimo 200 e no máximo 1.500 caracteres).'}
        )
    )


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

class LoginForm(forms.Form):
   
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nome de usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

# forms.py

from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))

# forms.py

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))

