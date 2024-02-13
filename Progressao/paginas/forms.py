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
            attrs={'class': 'textarea', 'placeholder': 'Digite aqui seu texto.'}
        )
    )


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
#----------------------------------------------------------------
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django import forms

class EmailForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Um usuário com este e-mail já existe.")
        return email

class NameForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'}),
        label='Primeiro Nome'
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Último Nome'}),
        label='Último Nome'
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']
   

class CustomUserCreationForm(SetPasswordForm):
    password1 = forms.CharField(
        
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Nova senha'
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}),
        label='Confirme a nova senha'
    )
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']

    def save(self, commit=True, **kwargs):
    # Assuming email, first_name, and last_name are passed in kwargs
        email = kwargs.pop('email', '')  # Extract email from kwargs
        first_name = kwargs.pop('first_name', '')  # Extract first_name
        last_name = kwargs.pop('last_name', '')  # Extract last_name

        user = CustomUser(email=email, first_name=first_name, last_name=last_name)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



from django import forms
from django.contrib.auth.password_validation import validate_password

# Em seu forms.py
from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserPasswordCreationForm(forms.Form):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        validate_password(password2)
        return password2

    def save(self, commit=True, **kwargs):
        user = CustomUser(
            email=kwargs.get('email', ''),
            first_name=kwargs.get('first_name', ''),
            last_name=kwargs.get('last_name', '')
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



#---------------------------------------------------------------------------------------------------------------------


from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new_password', 'placeholder': 'Senha'}),
    )
    
    new_password2 = forms.CharField(
        label="Confirme a nova senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new_password', 'placeholder': 'Confirmar Senha'}),
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


#-----------------------------------------------------------------------
    
    from django import forms

class PasswordResetView(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )