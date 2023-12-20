from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
from django.contrib.auth.views import PasswordResetConfirmView
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from paginas.forms import CustomPasswordResetConfirmForm
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_protect
from django.utils.http import urlsafe_base64_decode
from paginas.models import Test, Noun, Dicionario
from paginas.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .forms import MeuForm
from .models import Noun
import logging
import spacy
import csv
import numpy as np
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from django.shortcuts import render
import sys

#sys.path.append('home/milenasilva/Chat_ibict/Progressao/')
sys.path.append('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao')
from englishBackend.main import get_remote_works

from rpy2.robjects import pandas2ri
from rpy2 import robjects
import pandas as pd
import psycopg2
import h2o
from multiprocessing import Process


import rpy2.robjects as ro

import rpy2.robjects as robjects

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2 import robjects

import psycopg2
import h2o
from django.shortcuts import render
from paginas.forms import MeuForm
from paginas.models import Noun, Dicionario, Test

import psycopg2
import h2o
import csv
import numpy as np
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
@login_required
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


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
# from .forms import CustomLoginForm

# class CustomLoginForm(AuthenticationForm):
#     username = forms.EmailField(widget=forms.EmailInput(
#         attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': 'Senha'}))


logger = logging.getLogger(__name__)


from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import LoginForm  # Importe o formulário de login
@login_required
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Login bem-sucedido'})
            else:
                return JsonResponse({'success': False, 'message': 'Nome de usuário ou senha inválidos'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logger.info('Logout request received')
    logout(request)
    logger.info('User logged out successfully')
    return redirect('login')

# Para a view password_reset
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render

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
    return render(request, 'password_reset.html', {'form': form})

# Para a view reset_confirm
from django.contrib.auth import get_user_model, tokens
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from .forms import CustomPasswordResetConfirmForm

User = get_user_model()

def reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = CustomPasswordResetConfirmForm(user)
    else:
        return render(request, 'password_reset_invalid_link.html')

    return render(request, 'password_reset_confirm.html', {'form': form})

from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

class CustomPasswordResetConfirmForm(SetPasswordForm):
    # Adicione quaisquer campos ou lógicas personalizadas aqui

    # Exemplo: Adicionar um campo personalizado
    custom_field = forms.CharField(max_length=100, required=False, help_text=_("Campo personalizado"))

    # Exemplo: Sobrescrever o método clean para adicionar validações personalizadas
    def clean(self):
        cleaned_data = super().clean()
        custom_field_data = cleaned_data.get("custom_field")

        # Adicione sua lógica de validação aqui
        if custom_field_data and not custom_field_data.isalpha():
            self.add_error('custom_field', _("O campo personalizado deve conter apenas letras."))

        return cleaned_data

    # Exemplo: Sobrescrever o método save para adicionar lógicas adicionais após salvar
    def save(self, commit=True):
        user = super().save(commit=False)
        # Adicione sua lógica personalizada aqui
        # Exemplo: Atualizar um campo personalizado do usuário
        user.custom_attribute = self.cleaned_data.get('custom_field')

        if commit:
            user.save()
        return user

def get_df():

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
        query = """
                SELECT "idSignificado"
                FROM paginas_noun
                WHERE "idSignificado" != '' AND test_id = (
                    SELECT MAX ("test_id")
                    FROM paginas_noun);
                """
        cursor.execute(query)

        # Recupera os resultados da consulta como uma lista de tuplas
        # Recupera os resultados da consulta como uma lista de tuplas
        results = cursor.fetchall()

        for id in range(len(results)):
            results[id] = 'v'+results[id][0]
        # Fecha o cursor e a conexão
        cursor.close()
        # teste
        file = open("C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/modelos/todos_IDSignificados.Ocorrencias.csv", "r")
        #file = open("/home/milenasilva/Chat_ibict/Progressao/static/modelos/todos_IDSignificados.Ocorrencias.csv", "r")
        idsignificado = list(csv.reader(file, delimiter=","))
        file.close()

        idsignificado = [row[0] for row in idsignificado]

        for id in range(len(idsignificado)):
            idsignificado[id] = 'v'+idsignificado[id]

        df = pd.DataFrame(np.zeros((1, len(idsignificado))),
                          columns=idsignificado)
        df = df.astype(int)

        for id in results:
            df[id] = df[id] + 1

        with localconverter(robjects.default_converter + pandas2ri.converter):
            df = robjects.conversion.py2rpy(df)

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if 'connection' in locals():
            connection.close()

    return df


def get_best_models(area):
    try:
        connection = psycopg2.connect(
            database="testy",
            user="postgres",
            password="SENHA",
            host="127.0.0.1",
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
        df_modelos = pd.DataFrame(
            results, columns=[desc[0] for desc in cursor.description])

        # Fecha o cursor e a conexão
        cursor.close()

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if 'connection' in locals():
            connection.close()

        return df_modelos


def get_indicadores(area, subarea, tipo, subtipo, mindocs, rangedocs):
    try:
        connection = psycopg2.connect(
            database="testy",
            user="postgres",
            password="SENHA",
            host="127.0.0.1",
            port="5432"
        )

        # Cria um cursor para executar consultas
        cursor = connection.cursor()

        # Executa a consulta
        query = f"""
                SELECT * FROM public.models
                    where("Tipo" ='{tipo}' AND
                        "Subtipo" = '{subtipo}' AND
                        "MinDocs" = {mindocs} AND
                        "RangeDocs" =  '{rangedocs}' AND 
                "Subarea" = '{subarea}' AND
                "Area" = '{area}')
                """
        cursor.execute(query)

        # Recupera os resultados da consulta como uma lista de tuplas
        results = cursor.fetchall()

        # Cria um DataFrame pandas com os resultados
        df_indicadores = pd.DataFrame(
            results, columns=[desc[0] for desc in cursor.description])
        df_indicadores = df_indicadores.drop(
            ['Tipo', 'Subtipo', 'MinDocs', 'RangeDocs', 'Subarea', 'Area'], axis=1)
        # Fecha o cursor e a conexão
        cursor.close()

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if 'connection' in locals():
            connection.close()

        return df_indicadores


def prevNN(abstract):
    localH2o = h2o.init(nthreads=-1)

    Modelo = h2o.load_model('C:/Users/milen/OneDrive/Documentos/DF/Modelos/DeepLearning_model_R_1670582405235_1')
    #Modelo = h2o.load_model('/home/milenasilva/Chat_ibict/Progressao/static/modelos/DeepLearning_model_R_1670582405235_1')

    prevNN = Modelo.predict(h2o.H2OFrame(abstract))

    return prevNN[0, 0]


def prevC50(dados, str_modelo):
    base = importr('base')
    C50 = importr('C50')

    c50_model = robjects.r['load'](str_modelo)
    c50_model = base.get(c50_model[0])

    prevC50 = C50.predict_C5_0(c50_model, newdata=dados)

    del base
    del C50
    del c50_model

    return prevC50.levels[prevC50[0]-1]


def prevRFranger(dados, str_modelo):
    base = importr('base')

    robjects.r['load'](str_modelo)

    predict_r_code = """
    predict_rf <- function(model, data) {
        library(ranger)
        predict(Modelo, data)
    }
    """
    predict_r = SignatureTranslatedAnonymousPackage(
        predict_r_code, "predict_rf")

    modelo = robjects.globalenv['Modelo']
    previsoes_r = predict_r.predict_rf(modelo, dados)
    previsoes = previsoes_r.rx2('predictions')

    del base
    del modelo
    del predict_r_code

    return previsoes.levels[previsoes[0]-1]


def prevRFtrad(dados, str_modelo):
    base = importr('base')
    rf = importr('randomForest')

    robjects.r['load'](str_modelo)
    Modelo = robjects.r['Modelo']

    predict = robjects.r('predict')

    prevRF_trad = predict(Modelo, data=dados)

    del rf
    del base
    del Modelo
    del predict

    return prevRF_trad.levels[prevRF_trad[0]-1]


def prevRpart(dados, str_modelo):
    base = importr('base')
    rpart = importr('rpart')

    robjects.r['load'](str_modelo)
    Modelo = robjects.r['Modelo']

    predict = robjects.r('predict')

    prevRpart = predict(Modelo, data=dados, type="class")

    del rpart
    del base
    del Modelo
    del predict

    return prevRpart.levels[prevRpart[0]-1]


def process_rpy2():

    da = get_df()
    entrada = da
    with localconverter(robjects.default_converter + pandas2ri.converter):
        entrada_h2o = robjects.conversion.rpy2py(entrada)
    area = prevNN(entrada_h2o)
    modelos = get_best_models(area)
    vetor_strings = []

    for i in modelos.index:
        if (str(modelos['Tipo'][i]) == "RF" and str(modelos['Subtipo'][i]) == "ranger"):
            str_modelo = "C:/Users/milen/OneDrive/Documentos/DF/Modelo/Modelo.RF.ranger.200x1x280.Ocorrencias.ResearchAreaSA.RData"
            #str_modelo = "/home/milenasilva/Chat_ibict/Progressao/static/modelos/Modelo.RF.ranger.200x1x280.Ocorrencias.ResearchAreaSA.RData"
            prev_sub = prevRFranger(entrada, str_modelo)
            vetor_strings.append(prev_sub)

        if (str(modelos['Tipo'][i]) == "RF" and str(modelos['Subtipo'][i]) == "trad"):
            str_modelo = "C:/Users/milen/OneDrive/Documentos/DF/Modelo/Modelo.RF.trad.200x1x280.Ocorrencias.RData"
            #str_modelo = "/home/milenasilva/Chat_ibict/Progressao/static/modelos/Modelo.RF.trad.200x1x280.Ocorrencias.RData"
            prev_sub = prevRFtrad(entrada, str_modelo)
            vetor_strings.append(prev_sub)

        if (str(modelos['Tipo'][i]) == "C50"):
            str_modelo = f"""C:/Users/milen/OneDrive/Documentos/DF/Modelo/Modelo.C50.trad.100x1x100.Ocorrencias.ResearchAreaSA.{area}.RData"""
            #str_modelo = f"""/home/milenasilva/Chat_ibict/Progressao/static/modelos/Modelo.C50.trad.100x1x100.Ocorrencias.ResearchAreaSA.{area}.RData"""
            prev_sub = prevC50(entrada, str_modelo)
            vetor_strings.append(f"""c("{prev_sub}", "{area}")""")

        if (str(modelos['Tipo'][i]) == "RPART"):
            str_modelo = "C:/Users/milen/OneDrive/Documentos/DF/Modelo/Modelo.Rpart.trad.200x1x320.Ocorrencias.RData"
            #str_modelo = "/home/milenasilva/Chat_ibict/Progressao/static/modelos/Modelo.Rpart.trad.200x1x320.Ocorrencias.RData"
            #prev_sub = prevRpart(entrada, str_modelo)
            vetor_strings.append(f"""c("{prev_sub}", "{area}")""")
    # Verifique se a lista não está vazia

    # Agora, você pode usar a variável 'area1' para fazer o que for necessário

    area1 = vetor_strings[0].split('",')[1].strip()
    subarea1 = vetor_strings[0].split('",')[0].strip()
    tipo1 = modelos['Tipo'][0]
    subtipo1 = modelos['Subtipo'][0]
    mindocs1 = modelos['MinDocs'][0]
    rangedocs1 = modelos['RangeDocs'][0]

    area2 = vetor_strings[1].split('",')[1].strip()
    subarea2 = vetor_strings[1].split('",')[0].strip()
    tipo2 = modelos['Tipo'][1]
    subtipo2 = modelos['Subtipo'][1]
    mindocs2 = modelos['MinDocs'][1]
    rangedocs2 = modelos['RangeDocs'][1]

    area3 = vetor_strings[2].split('",')[1].strip()
    subarea3 = vetor_strings[2].split('",')[0].strip()
    tipo3 = modelos['Tipo'][2]
    subtipo3 = modelos['Subtipo'][2]
    mindocs3 = modelos['MinDocs'][2]
    rangedocs3 = modelos['RangeDocs'][2]

    indicadores1 = get_indicadores(
        area1, subarea1, tipo1, subtipo1, mindocs1, rangedocs1)
    indicadores2 = get_indicadores(
        area2, subarea2, tipo2, subtipo2, mindocs2, rangedocs2)
    indicadores3 = get_indicadores(
        area3, subarea3, tipo3, subtipo3, mindocs3, rangedocs3)

    count_indicadores1 = (indicadores1 > indicadores2).sum()
    count_indicadores2 = (indicadores2 > indicadores1).sum()
    count_indicadores2_1 = (indicadores2 > indicadores1).sum()
    count_indicadores2_3 = (indicadores2 > indicadores3).sum()

    count_indicadores3_1 = (indicadores3 > indicadores1).sum()
    count_indicadores3_2 = (indicadores3 > indicadores2).sum()
    count_indicadores1_2 = (indicadores1 > indicadores2).sum()
    count_indicadores1_3 = (indicadores1 > indicadores3).sum()

    count_indicadores2_1 = (indicadores2 > indicadores1).sum()
    count_indicadores2_3 = (indicadores2 > indicadores3).sum()

    count_indicadores3_1 = (indicadores3 > indicadores1).sum()
    count_indicadores3_2 = (indicadores3 > indicadores2).sum()

    if vetor_strings[0] == vetor_strings[1]:

        return vetor_strings[0]

    elif vetor_strings[0] == vetor_strings[2]:

        return vetor_strings[0]

    elif vetor_strings[1] == vetor_strings[2]:

        return vetor_strings[2]

    elif vetor_strings[0] == vetor_strings[1]:
        print("A primeira e segunda string são iguais.")

        if pd.Series((count_indicadores3_1 > count_indicadores1_3), (count_indicadores3_2 > count_indicadores2_3)).any():
            return (vetor_strings[2])
        else:
            return (vetor_strings[0])

    elif vetor_strings[0] == vetor_strings[2]:
        print("A primeira e terceira string são iguais.")

        if pd.Series((count_indicadores2_1 > count_indicadores1_2), (count_indicadores2_3 > count_indicadores3_2)).any():
            return (vetor_strings[1])
        else:
            return (vetor_strings[0])

    elif vetor_strings[1] == vetor_strings[2]:
        print("A segunda e terceira string são iguais.")

        if pd.Series((count_indicadores1_2 > count_indicadores2_1), (count_indicadores1_3 > count_indicadores3_1)).any():
            return (vetor_strings[0])
        else:
            return (vetor_strings[2])

    else:
        print("As três strings são diferentes.")

        if pd.Series((count_indicadores1_2 > count_indicadores2_1), (count_indicadores1_3 > count_indicadores3_1)).all():
            return (vetor_strings[0])
        elif pd.Series((count_indicadores2_1 > count_indicadores1_2), (count_indicadores2_3 > count_indicadores3_2)).all():
            return (vetor_strings[1])
        elif pd.Series((count_indicadores3_1 > count_indicadores1_3), (count_indicadores3_2 > count_indicadores2_3)).all():
            return (vetor_strings[2])
        else:
            return (vetor_strings[0])


# Call the function within the main thread
output = process_rpy2()

# Use the output as needed
print(output,'aqui')  # You can replace this with the function you want to return the result to
nlp = spacy.load("pt_core_news_lg")


from django.shortcuts import render, redirect
from .forms import MeuForm
from .models import Noun, Dicionario
import spacy
import re

# Importações adicionais
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import User
import h2o
from django.shortcuts import render, redirect
from .forms import MeuForm
from .models import Noun, Dicionario
import spacy
import re

# Importações adicionais
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import User
import h2o
from django.shortcuts import render
from .forms import MeuForm
# Supondo que 'main' e 'process_rpy2' sejam importados de outro módulo
#from englishBackend import main
# from ... import process_rpy2
def home(request):
    show_prevrf = False
    if request.method == 'POST':
        print("POST request received")
        form = MeuForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form = form.save(commit=False)
            form.user = request.user
            # abstract = form.phraseTest.lower()
            # form.phraseTest = abstract
            abstract = form.title
            title = form.phraseTest
            form.save()

            # title = form.cleaned_data['title']
            # abstract = form.cleaned_data['phraseTest']
            action = request.POST.get('action')

            if action == 'pesquisar_en':
                result_eng = get_remote_works(title, abstract)
                if len(result_eng) < 2:
                    area = 'Área não encontrada'
                    subarea = 'Subarea não encontrada'
                else:
                    area = result_eng[1]
                    subarea = result_eng[0]
                print(area)
            else:
                # Inicialize o H2O e Spacy fora do loop
                h2o.init()
                nlp = spacy.load("pt_core_news_lg")

                # Processamento do texto
                doc = nlp(abstract)
                lemmas = [token.lemma_ for token in doc if token.pos_ in ['PROPN', 'NOUN']]
                for lemma in lemmas:
                    new_noun = Noun.objects.create(
                        nounText=lemma.lower(),
                        test=form,
                        idSignificado=''
                    )
                    words = new_noun.nounText.split()
                    for word in words:
                        dicionario = Dicionario.objects.filter(Palavra=word.lower()).first()
                        if dicionario:
                            new_noun.idSignificado = dicionario.IDSignificado
                            new_noun.user = request.user
                            new_noun.save()

                # Chame process_rpy2 após processar todos os lemas
                print("Chamando process_rpy2...")
                resultado = process_rpy2()
                if resultado:
                    print(f"Resultado de process_rpy2: {resultado}")
                    resultado_limpo = re.sub(r'^\w+\(|\)$|\"', '', resultado)
                    partes = resultado_limpo.split(',')
                    subarea = partes[0].strip()
                    area = partes[1].strip()

                # Preparando o contexto para o template
            context = {'area': area,'subarea': subarea}
            # context = {'area': area}
            return render(request, 'result.html', context)
        else:
            print("process_rpy2 não retornou resultado válido.")

    else:
        form = MeuForm()

    context = {'form': form, 'show_prevrf': show_prevrf}
    return render(request, 'home.html', context)
