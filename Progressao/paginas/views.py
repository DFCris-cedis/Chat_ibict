
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.signals import user_logged_in, user_logged_out
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
from django.contrib.auth.forms import AuthenticationForm
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
from .models import Test, CustomUser

from django.shortcuts import render

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


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
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


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

from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)








nlp = spacy.load("pt_core_news_lg")


def home(request):
    show_prevrf = False  # Inicialmente, a variável show_prevrf é False
    if request.method == 'POST':
        form = MeuForm(request.POST)
        if form.is_valid():
            form = form.save()  # Salva a mensagem no banco de dados

            phraseTest = form.phraseTest  # Salva o texto em uma variável Python
            phraseTest = phraseTest.lower()  # Transforma todas as palavras em minúsculas

            # Processar o texto com o spaCy
            doc = nlp(phraseTest)

            # ## extrair as palavras e seus lemas
            lemmas = [token.lemma_ for token in doc if token.pos_ in [
                'PROPN', 'NOUN']]
            words = [token.text for token in doc]
            pos_tags = [token.pos_ for token in doc]
            dep_tags = [token.dep_ for token in doc]

            # extrair as entidades nomeadas
            named_entities = [(ent.text, ent.label_) for ent in doc.ents]

            # extrair os sintagmas nominais
            noun_chunks = [np.text for np in doc.noun_chunks]

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

            context = {'form': form}  # Define o contexto para a página HTML

            return render(request, 'result.html', context)
    else:
        form = MeuForm()
    # Define o contexto para a página HTML
    context = {'form': form, 'show_prevrf': show_prevrf}
    return render(request, 'home.html', context)
