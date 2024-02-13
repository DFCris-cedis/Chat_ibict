import sys

#sys.path.append('/home/milenasilva/Chat_ibict/Progressao/')
sys.path.append('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao')

from django.contrib.auth.signals import user_logged_in, user_logged_out
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from rpy2.robjects.conversion import localconverter
from paginas.models import Test, Noun, Dicionario
from paginas.models import Noun, Dicionario, Test
from paginas.forms import CustomUserCreationForm
from englishBackend.main import get_remote_works
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from rpy2.robjects.packages import importr
from django.contrib.auth.forms import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.dispatch import receiver
from .models import Noun, Dicionario
from rpy2.robjects import pandas2ri
from multiprocessing import Process
from django.contrib import messages
from paginas.forms import MeuForm
import rpy2.robjects as robjects
from .forms import LoginForm
import rpy2.robjects as ro
from .forms import MeuForm
# from rpy2 import robjects
from .models import Noun
import pandas as pd
import numpy as np
import psycopg2
import logging
import spacy
import csv
import h2o
import re

User = get_user_model()
 

from django.shortcuts import render, redirect
from .forms import EmailForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
from .forms import UserPasswordCreationForm


def signup_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():
                # Se o e-mail já existir, adicione um erro ao formulário
                form.add_error('email', 'Um usuário com este e-mail já existe.')
            else:
                # O e-mail não existe no banco de dados, pode prosseguir com o cadastro
                # Salve o e-mail na sessão ou continue com o processo de cadastro
                request.session['email_for_signup'] = email
                return redirect('signup_name')  # Direcione para a próxima etapa do cadastro
        # Se o formulário não for válido ou se o e-mail já existir
        return render(request, 'signup_email.html', {'form': form})
    else:
        form = EmailForm()
        return render(request, 'signup_email.html', {'form': form})


from .forms import NameForm

def signup_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            return redirect('signup_password')
    else:
        form = NameForm()
    return render(request, 'signup_name.html', {'form': form})


def signup_password(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserPasswordCreationForm(request.POST)
        if form.is_valid():
            # Usar a chave correta para recuperar o e-mail da sessão
            email = request.session.get('email_for_signup')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')

            if not email:
                form.add_error(None, 'O campo de e-mail deve ser fornecido.')
                return render(request, 'signup_password.html', {'form': form})

            password = form.cleaned_data['password1']
            user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
            
            del request.session['email_for_signup'], request.session['first_name'], request.session['last_name']
            return redirect('home')
    else:
        form = UserPasswordCreationForm()

    return render(request, 'signup_password.html', {'form': form})


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

logger = logging.getLogger(__name__)

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm  # Supondo que LoginForm é importado corretamente

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import EmailForm


from paginas.models import CustomUser  # Importe seu modelo de usuário personalizado

def email_login(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomUser.objects.filter(email=email).exists():  # Use CustomUser aqui
                request.session['email_for_login'] = email
                return redirect('senha_login')
            else:
                return render(request, 'email_login.html', {'form': form, 'error': 'E-mail não encontrado'})
    else:
        form = EmailForm()
    return render(request, 'email_login.html', {'form': form})

# views.py

from django.contrib.auth import authenticate, login
from .forms import PasswordForm

def senha_login(request):
    email = request.session.get('email_for_login')
    if not email:
        # Redirecione para a página de e-mail se não houver e-mail na sessão
        return redirect('email_login')

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=email, password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # Redirecione para a página inicial ou painel após o login bem-sucedido
                return redirect('home')
            else:
                # Senha incorreta
                return render(request, 'senha_login.html', {'form': form, 'error': 'Senha incorreta'})
    else:
        form = PasswordForm()
    return render(request, 'senha_login.html', {'form': form})


def logout_view(request):
    logger.info('Logout request received')
    logout(request)
    logger.info('User logged out successfully')
    return redirect('login')


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

# Custom Password Reset View
class PasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'

# Custom Password Reset Done View
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

# Custom Password Reset Confirm View
from django.shortcuts import render

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser  # Ajuste conforme o caminho do seu modelo de usuário

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        # Check if the provided email exists in the system
        email = form.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "E-mail não existente, crie uma conta.")
            return render(self.request, self.template_name, {'form': form})

        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('home')  # Redireciona para a tela inicial após a redefinição da senha.
    form_class = SetPasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            uid = urlsafe_base64_decode(self.kwargs['uidb64']).decode()
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            self.user = None
        
        kwargs['user'] = self.user
        return kwargs



# Custom Password Reset Complete View
class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    


import psycopg2
import pandas as pd
import numpy as np
import csv

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
                    SELECT MAX("test_id")
                    FROM paginas_noun);
                """
        cursor.execute(query)

        results = cursor.fetchall()

        for id in range(len(results)):
            results[id] = 'v' + results[id][0]

        # Fecha o cursor e a conexão
        cursor.close()
        
        #file = open("/home/milenasilva/Chat_ibict/Progressao/static/modelos/todos_IDSignificados.Ocorrencias.csv", "r")
        file = open("C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/modelos/todos_IDSignificados.Ocorrencias.csv", "r")
       
        idsignificado = list(csv.reader(file, delimiter=","))
        file.close()

        idsignificado = ['v' + row[0] for row in idsignificado]

        df = pd.DataFrame(np.zeros((1, len(idsignificado))),
                          columns=idsignificado)
        df = df.astype(int)

        for id in results:
            df[id] = df[id] + 1

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        if 'connection' in locals():
            connection.close()

    return df

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import pandas as pd
import psycopg2
import warnings
import joblib
import h2o
import time

warnings.simplefilter("ignore")
localH2o = h2o.init(nthreads = -1)

def get_best_models(area, quant):
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
                SELECT "model", "algorithm", "accuracy", "precision", "recall", "f1-score" FROM public.metrics
                WHERE "area" = '{area}'
                ORDER BY "f1-score" DESC LIMIT {quant};
                """
        cursor.execute(query)

        # Recupera os resultados da consulta como uma lista de tuplas
        results = cursor.fetchall()

        # Cria um DataFrame pandas com os resultados
        df_modelos = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

        # Fecha o cursor e a conexão
        cursor.close()

    except psycopg2.Error as error:
        print("Erro ao conectar ao PostgreSQL:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if 'connection' in locals():
            connection.close()
        
        return df_modelos
    
def get_prevision(row, entrada):
    modelo = row[1]

    if modelo == "Random Forest" :
        #resultado = prevRF(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevRF(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'AdaBoost':
        #resultado = prevADA(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevADA(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'XGBoost':
        #resultado = prevXGB(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevXGB(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'CatBoost':
        #resultado = prevCAT(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevCAT(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'Decision Tree':
        #resultado = prevDT(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevDT(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'GaussianNB':
        #resultado = prevGNB(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevGNB(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    if modelo == 'Logistic Regression':
        #resultado = prevLOG(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevLOG(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        
    if modelo == 'SVC':
        #resultado = prevSVC(entrada, ('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/' + row[0]))
        resultado = prevSVC(entrada, ('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/' + row[0]))

    return resultado

def prevH2O(abstract):
    #model = h2o.load_model('/home/milenasilva/Chat_ibict/Progressao/static/modelos/DeepLearning_model_R_1670582405235_1')
    model = h2o.load_model('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/DeepLearning_model_R_1670582405235_1')
    prev = model.predict(h2o.H2OFrame(abstract))
    del(model)
    return prev[0, 0]

def prevXGB(abstract, path_model):
    model, encoder, _, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevADA(abstract, path_model):
    model, encoder, _, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevCAT(abstract, path_model):
    model, _= joblib.load(path_model)
    
    prev = model.predict(abstract)
    del(model)
    return prev[0][0]

def prevDT(abstract, path_model):
    model, encoder, _, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevGNB(abstract, path_model):
    model, encoder, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevLOG(abstract, path_model):
    model, encoder, _, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevSVC(abstract, path_model):
    model, encoder, _, _ = joblib.load(path_model)
    
    prev = model.predict(abstract)

    label_encoder = LabelEncoder()
    label_encoder.fit_transform(encoder)
    
    prev = label_encoder.inverse_transform(prev)
    del(model, encoder)
    return prev[0]

def prevRF(abstract, path_model):
    model, _= joblib.load(path_model)
    
    prev = model.predict(abstract)
    del(model)
    return prev[0]

# def prev(entrada, qnt_models = 5):
#     start = time.time()
    
#     area = prevH2O(entrada)
    
#     models = get_best_models(area, min(qnt_models, 8))
    
#     results = []
    
#     for index, row in models.iterrows():
#         results.append(get_prevision(row, entrada))
    

#     map = {}

#     for i, result in enumerate(results):
#         map[result] = map.get(result, 0) + models['f1-score'][i]
        
#     sub, max_value = max(map.items(), key=lambda x: x[1])

#     ans = [sub, area]
    
#     # ans_total_values = ans.append(results)
#     # print(ans_total_values)
#     # end = time.time()
#     # print(f"""tempo total para previsão {end - start}s""")
    
#     return ans

# path_df = 'C:/Users/milen/OneDrive/Documentos/df.100x1x100.Ocorrencias.csv'
# df_id = 'eef474adc4c2d494dca53fa6b3bd8211'

# df = pd.read_csv(path_df)

# df.head(1)

# entrada = df.tail(1)
# entrada = entrada.drop(['Status'], axis=1)

# entrada
def prev(entrada, qnt_models=5):
    start = time.time()

    area = prevH2O(entrada)

    models = get_best_models(area, min(qnt_models, 8))

    results = []

    for index, row in models.iterrows():
        results.append(get_prevision(row, entrada))

    map = {}

    for i, result in enumerate(results):
        map[result] = map.get(result, 0) + models['f1-score'][i]

    # Check if map is not empty
    if map:
        sub, max_value = max(map.items(), key=lambda x: x[1])
    else:
        # Handle the empty case - either set default values, or handle it differently
        sub, max_value = "Não Encontrado", 0  # Example default values

    ans = [sub, area]

    # ans_total_values = ans.append(results)
    # print(ans_total_values)
    # end = time.time()
    # print(f"""tempo total para previsão {end - start}s""")
    ans_total_values = ans + results

    # Print combined results
    print("Combined Results:", ans_total_values)

    end = time.time()
    print(f"Total time for prediction: {end - start}s")

    return ans

# prev(entrada)
def process():

    da = get_df()
    entrada = da
    result = prev(entrada)
    return result

output = process()

print(output,'aqui')  # You can replace this with the function you want to return the result to
nlp = spacy.load("pt_core_news_lg")

def home(request):
    show_prevrf = False
    if request.method == 'POST':
        print("POST request received")
        form = MeuForm(request.POST)
        if form.is_valid():

            print("Form is valid")
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()
            abstract = form_instance.phraseTest.lower()
            title = form_instance.title
            form.save()

            language = request.POST.get('language')
            print(language)
            if language == 'en':
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
                # h2o.init()
                nlp = spacy.load("pt_core_news_lg")

                # Processamento do texto
                doc = nlp(abstract)  # Usando 'abstract', que é o 'phraseTest' em minúsculas
                lemmas = [token.lemma_ for token in doc if token.pos_ in ['PROPN', 'NOUN']]
                for lemma in lemmas:
                    new_noun = Noun.objects.create(
                        nounText=lemma.lower(),
                        test=form_instance,
                        idSignificado=''
    )
                    words = new_noun.nounText.split()
                    for word in words:
                        dicionario = Dicionario.objects.filter(Palavra=word.lower()).first()
                        if dicionario:
                            new_noun.idSignificado = dicionario.IDSignificado
                            new_noun.user = request.user
                            new_noun.save()

                # Chame process após processar todos os lemas
                print("Chamando process...")
                
                resultado = process()
                if resultado:
                    print(f"Resultado de process: {resultado}")
                    # cleaned_string = re.sub(r"^\['c\(\"|\"\)\']$", '', resultado)
                    # resultados = re.split(r'",\s*"', cleaned_string)
                    # print(type(resultado_limpo))
                    # partes = resultado_limpo.split(',')
                    # subarea = resultado[0].strip()
                    # area = resultado[1].strip()
                    
                    subarea = resultado[0]
                    area = resultado[1]
                    

                # Preparando o contexto para o template
            context = {'area': area,'subarea': subarea}
            # context = {'area': area}
            return render(request, 'result.html', context)
        else:
            print("process não retornou resultado válido.")

    else:
        form = MeuForm()

    context = {'form': form, 'show_prevrf': show_prevrf}
    return render(request, 'home.html', context)

def conheca_mais(request):
    return render(request, 'conheca_mais.html')

def contate_nos(request):
    return render(request, 'contate_nos.html')