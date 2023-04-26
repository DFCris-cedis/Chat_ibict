from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
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
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'E-mail'})
    )

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         user_exists = CustomUser.objects.filter(email=email).exists()
#         if not user_exists:
#             raise forms.ValidationError(
#                 'Este e-mail não está associado a nenhuma conta.')
#         return email


# class CustomPasswordResetFormLayout(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(
#         attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'E-mail'}))


# class CustomPasswordResetForm(PasswordResetForm):
#     # Adicione quaisquer campos adicionais necessários ao formulário de redefinição de senha aqui
#     pass


# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     email_template_name = 'password_reset_email.html'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'password_reset.html'

#     def form_valid(self, form):
#         form.save(
#             domain_override='example.com',
#             subject_template_name='password_reset_subject.txt',
#             use_https=self.request.is_secure(),
#             request=self.request
#         )
#         return super().form_valid(form)


# class PasswordResetDoneView(FormView):
#     template_name = 'password_reset_done.html'
#     success_url = reverse_lazy('login')
