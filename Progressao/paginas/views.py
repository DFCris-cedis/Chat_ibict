from .forms import MeuForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from paginas.models import Test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import logout
import logging
from django import forms
from django.dispatch import receiver
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# from .forms import CreateUserForm, LoginForm
from paginas.models import Test, Noun, Dicionario
import spacy
from django.shortcuts import render
from django.views.generic import ListView
from .models import Test


from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

from .models import ResultML
import spacy
from django.shortcuts import render
from .forms import MeuForm
from .models import Noun
import time
from .models import Test


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=user.email, password=raw_password)
            login(request, user)
            return redirect('home')
           # return render(request, 'login.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def home(request):
    if request.method == 'POST':
        teste = Test(titulo=request.POST['titulo'], idUser=request.user)
        teste.save()
        return render(request, 'home.html')
    else:
        testes = Test.objects.all().filter(idUser_id=request.user)
        return render(request, 'home.html', {'testes': testes})


# @login_required
# def home(request):
#     if request.method == 'POST':
#         form = MeuForm(request.POST)
#         if form.is_valid():
#             teste = form.save(commit=False)
#             teste.idUser = request.user
#             teste.save()
#         else:
#             print(form.errors)  # debug code
#     else:
#         form = MeuForm()
#     return render(request, 'home.html', {'form': form})


@receiver(user_logged_in)
def login_success(sender, user, request, **kwargs):
    user.is_staff = True
    user.save()


@receiver(user_logged_out)
def logout_success(sender, user, request, **kwargs):
    user.is_staff = False
    user.save()


@login_required
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user.is_active = True
            user.save()
            return redirect('home')
        else:
            error_message = 'Nome de usuário ou senha inválidos.'
    else:
        form = CustomLoginForm()
        error_message = ''
    return render(request, 'login.html', {'form': form, 'error_message': error_message})


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Senha'}))


logger = logging.getLogger(__name__)


def logout_view(request):
    logger.info('Logout request received')
    logout(request)
    logger.info('User logged out successfully')
    return redirect('login')


User = get_user_model()


def recuperar_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass  # Lidar com o usuário não encontrado
        else:
            # Criar token de redefinição de senha
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())

            # Criar link de redefinição de senha
            reset_link = f"{settings.BASE_URL}/password_reset_email/{uid}/{token}/"

            # Renderizar o template de email de redefinição de senha
            message = render_to_string('password_reset_email.html', {
                'reset_link': reset_link,
            })

            # Enviar o email
            send_mail(
                'Recuperação de senha',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            # Lidar com o email enviado com sucesso
    else:
        # Renderizar o formulário de recuperação de senha
        return render(request, 'password_reset_email.html')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise forms.ValidationError(
                'Este e-mail não está associado a nenhuma conta.')
        return email


def save_search(request):
    if request.method == 'POST':
        phrase = request.POST['phrase']
        test = Test(phraseTest=phrase, idUser=request.user)
        test.save()
        return redirect('search_results')
    else:
        return render(request, 'search_form.html')


nlp = spacy.load("pt_core_news_lg")


# def home(request):
#     show_prevrf = False  # Inicialmente, a variável show_prevrf é False
#     if request.method == 'POST':
#         form = MeuForm(request.POST)
#         if form.is_valid():
#             form = form.save()  # Salva a mensagem no banco de dados


#             phraseTest = form.phraseTest  # Salva o texto em uma variável Python
#             phraseTest = phraseTest.lower()  # Transforma todas as palavras em minúsculas

#             # Processar o texto com o spaCy
#             doc = nlp(phraseTest)

#             # ## extrair as palavras e seus lemas
#             lemmas = [token.lemma_ for token in doc if token.pos_ in [
#                 'PROPN', 'NOUN']]
#             words = [token.text for token in doc]
#             pos_tags = [token.pos_ for token in doc]
#             dep_tags = [token.dep_ for token in doc]

#             # extrair as entidades nomeadas
#             named_entities = [(ent.text, ent.label_) for ent in doc.ents]

#             # extrair os sintagmas nominais
#             noun_chunks = [np.text for np in doc.noun_chunks]

#             for lemma in lemmas:
#                 new_noun = Noun.objects.create(
#                     nounText=lemma, test=form, idSignificado='')

#                 words = new_noun.nounText.split()
#                 for word in words:
#                     dicionario = Dicionario.objects.filter(
#                         Palavra=word).first()
#                     if dicionario:
#                         new_noun.idSignificado = dicionario.IDSignificado
#                         new_noun.save()

#             context = {'form': form}  # Define o contexto para a página HTML

#             return render(request, 'result.html', context)
#     else:
#         form = MeuForm()
#     # Define o contexto para a página HTML
#     context = {'form': form, 'show_prevrf': show_prevrf}
#     return render(request, 'form.html', context)
@login_required
def home(request):
    if request.method == 'POST':
        form = MeuForm(request.POST)
        if form.is_valid():
            # Cria um objeto Teste associado ao usuário atual
            form = form.save(commit=False)
            form.idUser = request.user
            form.save()

            phraseTest = form.phraseTest.lower()

            doc = nlp(phraseTest)

            lemmas = [token.lemma_ for token in doc if token.pos_ in [
                'PROPN', 'NOUN']]

            for lemma in lemmas:
                new_noun = Noun.objects.create(
                    nounText=lemma, test=form, idSignificado='')

                words = new_noun.nounText.split()
                for word in words:
                    dicionario = Dicionario.objects.filter(
                        Palavra=word).first()
                    if dicionario:
                        new_noun.idSignificado = dicionario.IDSignificado
                        new_noun.save()

            context = {'form': form}

            return render(request, 'result.html', context)
        else:
            # Adicione logs para ajudar a diagnosticar problemas
            print("Formulário inválido:", form.errors)
    else:
        form = MeuForm()
    context = {'form': form}
    return render(request, 'form.html', context)
