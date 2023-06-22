from django.contrib.auth.forms import PasswordResetForm
from .models import CustomUser
from django import forms
from .models import Test
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

from django import forms
from .models import Test


# class TesteForm(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['testId', 'phraseTest', 'idUser']


class MeuForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['phraseTest']
    phraseTest = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': 'Digite aqui seu texto'}))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

# from django import forms
# from django.contrib.auth.forms import PasswordResetForm

# class CustomPasswordResetForm(PasswordResetForm):
#     email = forms.EmailField(
#         max_length=254,
#         widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
#     )

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         user_exists = CustomUser.objects.filter(email=email).exists()
#         if not user_exists:
#             raise forms.ValidationError('Este e-mail não está associado a nenhuma conta.')
#         return email


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'E-mail'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = CustomUser.objects.filter(email=email).exists()
        if not user_exists:
            raise forms.ValidationError(
                'Este e-mail não está associado a nenhuma conta.')
        return email


class CustomPasswordResetFormLayout(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'E-mail'}))

