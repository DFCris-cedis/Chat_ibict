from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from paginas.forms import CustomPasswordResetConfirmForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_protect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import views as auth_views
from paginas.models import Test, Noun, Dicionario
from paginas.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.dispatch import receiver
from django import forms
from .forms import MeuForm
from .models import Noun
import logging
import spacy


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
# def home(request):
#     return render(request, 'home.html')
def home(request):
    if request.method == 'POST':
        phrase = request.POST.get('phrase', '')
        # Pega o usuário logado
        user = request.user
        # Cria uma nova instância de Test com a foreign key do usuário
        Test.objects.create(user=user, phraseTest=phrase)
    
    tests = Test.objects.filter(user=request.user)
    return render(request, 'home.html', {'tests': tests})


@receiver(user_logged_in)
def login_success(sender, user, request, **kwargs):
    user.is_staff = True
    user.save()


@receiver(user_logged_out)
def logout_success(sender, user, request, **kwargs):
    user.is_staff = False
    user.save()


# @login_required
# def login_view(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             user.is_active = True
#             user.save()
#             return redirect('home')
#         else:
#             error_message = 'Nome de usuário ou senha inválidos.'
#     else:
#         form = CustomLoginForm()
#         error_message = ''
#     return render(request, 'login.html', {'form': form, 'error_message': error_message})

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from .forms import CustomLoginForm


def login_view(request):
    
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                user.is_active = True
                user.save()
                return redirect('home')
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


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def get(self, request, *args, **kwargs):
        # Define o atributo user no objeto de request
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        setattr(request, 'user', user)

        # Chama o método get() da superclasse
        return super().get(request, *args, **kwargs)


@csrf_protect
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email='from@example.com',
                email_template_name='password_reset_email.html'
            )
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})


def reset_confirm(request, uidb64, token):
    form_class = CustomPasswordResetConfirmForm
    validlink = True
    user = auth_views.PasswordResetConfirmView().get_user(uidb64)
    if user is None:
        validlink = False
    else:
        if not auth_views.PasswordResetConfirmView().token_generator.check_token(user, token):
            validlink = False
    if validlink:
        if request.method == 'POST':
            form = form_class(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = form_class(user)
        return render(request, 'password_reset_confirm.html', {'form': form, 'validlink': validlink})


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
#                         new_noun.user = request.user  # Atribui o usuário atual à coluna 'user'
#                         new_noun.save()
#             context = {'form': form}  # Define o contexto para a página HTML

#             return render(request, 'result.html', context)
#     else:
#         form = MeuForm()
#     # Define o contexto para a página HTML
#     context = {'form': form, 'show_prevrf': show_prevrf}
#     return render(request, 'home.html', context)

from django.shortcuts import render
from paginas.forms import MeuForm
from paginas.models import Noun, Dicionario, Test


# def home(request):
#     show_prevrf = False  # Inicialmente, a variável show_prevrf é False
#     if request.method == 'POST':
#         form = MeuForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.user = request.user # Atribui o usuário atual ao atributo 'user'
#             form.save() 

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
#                         new_noun.user = request.user  # Atribui o usuário atual à coluna 'user'
#                         new_noun.save()

#             context = {'form': form}  # Define o contexto para a página HTML

#             return render(request, 'result.html', context)
#     else:
#         form = MeuForm()
#     # Define o contexto para a página HTML
#     context = {'form': form, 'show_prevrf': show_prevrf}
#     return render(request, 'home.html', context)
nlp = spacy.load("pt_core_news_lg")
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

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

# #             # extrair as entidades nomeadas
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
#                         new_noun.user = request.user # Atribui o usuário atual à coluna 'user'
#                         new_noun.save()

           
#             context = {'form': form}  # Define o contexto para a página HTML

#             return render(request, 'result.html', context)
#     else:
#         form = MeuForm()
#      # Define o contexto para a página HTML
#     context = {'form': form, 'show_prevrf': show_prevrf}
#     return render(request, 'home.html', context)


#------------------------------------------------------------------------teste

from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2 import robjects
import pandas as pd
import psycopg2
import h2o

def get_best_models(area):
    try:
        connection = psycopg2.connect(
            database="testy",
            user="postgres",
            password="SENHA",
            host="localhost",
            port="5432"
        )

        # Cria um cursor para executar consultas
        cursor = connection.cursor()

        # Executa a consulta
        query = f"""
                SELECT "Tipo", "Subtipo", "MinDocs", "RangeDocs", COUNT(*)
                FROM(
                    SELECT * FROM public.models
                    WHERE ("Subarea", "F1") IN (

                      SELECT "Subarea", MAX("F1") AS max_f1

                      FROM public.models
                      WHERE "Area" = '{area}' AND "Subtipo" != 'ranger'

                      GROUP BY "Subarea"

                    )
                    ORDER BY "F1" DESC
                ) as tabela

                GROUP BY "Tipo", "Subtipo", "MinDocs", "RangeDocs"
                ORDER BY COUNT(*) DESC
                LIMIT 3
                """
        cursor.execute(query)

        # Recupera os resultados da consulta como uma lista de tuplas
        results = cursor.fetchall()

        # Cria um DataFrame pandas com os resultados
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Fecha o cursor e a conexão
        cursor.close()

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if 'connection' in locals():
            connection.close()
        
        return df



def prevNN(abstract):
    localH2o = h2o.init(nthreads = -1)
    
    Modelo = h2o.load_model('C:/Users/milen/OneDrive/Documentos/DF/Modelos/DeepLearning_model_R_1670582405235_1')
    prevNN = Modelo.predict(h2o.H2OFrame(abstract))
    
    return prevNN[0, 0]

def prevC50(dados, str_modelo):
    base = importr('base')
    utils = importr('utils') 
    C50 = importr('C50')
    
    robjects.r['load']('C:/Users/milen/OneDrive/Documentos/DF/Modelos/' + str_modelo)
    Modelo = robjects.r['Modelo']
    
    predict = robjects.r('predict')
    
    prevC50 = predict(Modelo, type = "class", newdata = dados)
    
    del C50
    del utils
    del base
    del Modelo
    del predict
    
    return prevC50.levels[prevC50[0]-1]

def prevRFranger(dados, str_modelo):
    base = importr('base')
    utils = importr('utils')    
    ranger = importr('ranger')
    
    robjects.r['load']('C:/Users/milen/OneDrive/Documentos/DF/Modelos/' + str_modelo)
    Modelo = robjects.r['Modelo']
    
    predict = robjects.r('predict')
    
    prevRF_ranger = predict(Modelo, data = dados)
    prevRF_ranger = prevRF_ranger[0]
    
    del ranger
    del utils
    del base
    del Modelo
    del predict
    
    return prevRF_ranger.levels[prevRF_ranger[0]-1]

def prevRFtrad(dados, str_modelo):
    base = importr('base')
    utils = importr('utils')    
    rf = importr('randomForest')
    
    robjects.r['load']('C:/Users/milen/OneDrive/Documentos/DF/Modelos/' + str_modelo)
    Modelo = robjects.r['Modelo']
    
    predict = robjects.r('predict')
    
    prevRF_trad = predict(Modelo, data = dados)
    
    del rf
    del utils
    del base
    del Modelo
    del predict
    
    return prevRF_trad.levels[prevRF_trad[0]-1]

def prevRpart(dados, str_modelo):
    base = importr('base')
    utils = importr('utils')    
    rpart= importr('rpart')
    
    robjects.r['load']('C:/Users/milen/OneDrive/Documentos/DF/Modelos/' + str_modelo)
    Modelo = robjects.r['Modelo']
    
    predict = robjects.r('predict')
    
    prevRpart = predict(Modelo, data = dados, type="class")
    
    del rpart
    del utils
    del base
    del Modelo
    del predict
    
    prevRpart.levels[prevRpart[0]-1]

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required


# Chamar a função prevNN



@login_required  # Requer autenticação do usuário
def home(request):
    show_prevrf = False  # Inicialmente, a variável show_prevrf é False
    if request.method == 'POST':
        form = MeuForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user # Atribui o usuário atual ao atributo 'user'
            form.save() 
            
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
                        new_noun.user = request.user  # Atribui o usuário atual à coluna 'user'
                        new_noun.save()

                # Executar código adicional
            try:
                base = importr('base')
                utils = importr('utils')

                robjects.r['load']('Modelos/df.100x1x100.Ocorrencias.Rdata')
                dados_df = robjects.r['dados.df']

                with localconverter(robjects.default_converter + pandas2ri.converter):
                    df = robjects.conversion.rpy2py(dados_df)

                entrada = df.loc[['eef474adc4c2d494dca53fa6b3bd8211']]
                del entrada['Status']
                print(area)
                modelos = get_best_models(area)

                with localconverter(robjects.default_converter + pandas2ri.converter):
                    dados = robjects.conversion.py2rpy(entrada)

                subareas = []

                for i in modelos.index:
                    str_modelo = "Modelo." + str(modelos['Tipo'][i]) + "." + str(modelos['Subtipo'][i]) + "." + str(modelos['MinDocs'][i]) + "x" + str(modelos['RangeDocs'][i]) + ".Ocorrencias.ResearchAreaSA." + area + ".RData"

                    if(str(modelos['Tipo'][i]) == "RF" and str(modelos['Subtipo'][i]) == "ranger"):
                        prev_sub = prevRFranger(dados, str_modelo)
                        subareas.append(prev_sub)

                    if(str(modelos['Tipo'][i]) == "RF" and str(modelos['Subtipo'][i]) == "trad"):
                        str_modelo = "Modelo." + str(modelos['Tipo'][i]) + "." + str(modelos['Subtipo'][i]) + "." + str(modelos['MinDocs'][i]) + "x" + str(modelos['RangeDocs'][i]) + ".Ocorrencias.RData"

                        prev_sub = prevRFtrad(dados, str_modelo)
                        subareas.append(prev_sub)

                    if(str(modelos['Tipo'][i]) == "C50"):
                        prev_sub = prevC50(dados, str_modelo)
                        subareas.append(prev_sub)

                    if(str(modelos['Tipo'][i]) == "RPART"):
                        prev_sub = prevRpart(dados, str_modelo)
                        subareas.append(prev_sub)

                show_prevrf = True  # Define show_prevrf como True para exibir os resultados
                print(subareas)

            except Exception as e:
                print("Erro durante a execução do código:", e)

    else:
        form = MeuForm()

    context = {
        'form': form,
        'show_prevrf': show_prevrf,
    }

    return render(request, 'home.html', context)
 