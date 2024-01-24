import sys
sys.path.append('/home/milenasilva/Chat_ibict/Progressao/')
#sys.path.append('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao')

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

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None

        if self.user is not None and self.token_generator.check_token(self.user, kwargs['token']):
            return super().dispatch(*args, **kwargs)
        else:
            # Redireciona para a tela de login
            return HttpResponseRedirect(reverse('login'))

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
        
        #file = open("C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/todos_IDSignificados.Ocorrencias.csv", "r")
        file = open("/home/milenasilva/Chat_ibict/Progressao/static/modelos/todos_IDSignificados.Ocorrencias.csv", "r")
       
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
import pandas as pd
import warnings
import joblib
import h2o

warnings.simplefilter("ignore")

def prevNN(abstract):
    localH2o = h2o.init(nthreads=-1)
    
    #Modelo = h2o.load_model("C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/DeepLearning_model_R_1670582405235_1")
    Modelo = h2o.load_model("/home/milenasilva/Chat_ibict/Progressao/static/modelos/DeepLearning_model_R_1670582405235_1")
    
    prevNN = Modelo.predict(h2o.H2OFrame(abstract))
    
    return prevNN[0, 0]

def prevXGB(abstract, path_modelo):
    modelo = joblib.load(path_modelo)
    prevXGB = modelo.predict(abstract)

    return prevXGB


def process():

    da = get_df()
    entrada = da

    area = prevNN(entrada)
   
    print(area)

    if area == 'CIENCIAS SOCIAIS APLICADAS':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasSociaisAplicadas_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasSociaisAplicadas.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasSociaisAplicadas_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasSociaisAplicadas.csv')

    if area == 'CIENCIAS DA SAUDE':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasDaSaude_xgboost.pkl'
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasDaSaude.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasDaSaude_xgboost.pkl'
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasDaSaude.csv')
        
    if area == 'LINGUISTICA, LETRAS E ARTES':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/LinguisticaLetrasArtes_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_LinguisticaLetrasArtes.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/LinguisticaLetrasArtes_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_LinguisticaLetrasArtes.csv')
        
    if area == 'CIENCIAS EXATAS E DA TERRA':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasExatasDaTerra_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasExatasDaTerra.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasExatasDaTerra_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasExatasDaTerra.csv')
        
    if area == 'MULTIDISCIPLINAR':
        # #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/Multidisciplinar_xgboost.pkl' 
        # #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_Multidisciplinar.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/Multidisciplinar_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_Multidisciplinar.csv')
        
    if area == 'CIENCIAS HUMANAS':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasHumanas_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasHumanas.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasHumanas_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasHumanas.csv')
        
    if area == 'ENGENHARIAS':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/Engenharias_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_Engenharias.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/Engenharias_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_Engenharias.csv')
        
    if area == 'CIENCIAS BIOLOGICAS':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasBiologicas_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasBiologicas.csv')
        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasBiologicas_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasBiologicas.csv')
        
    if area == 'CIENCIAS AGRARIAS':
        #path_model = 'C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/CienciasAgrarias_xgboost.pkl' 
        #encoder = pd.read_csv('C:/Users/milen/OneDrive/Documentos/GitHub/Chat_ibict/Progressao/static/Modelos/encoder_CienciasAgrarias.csv')

        path_model = '/home/milenasilva/Chat_ibict/Progressao/static/Modelos/CienciasAgrarias_xgboost.pkl' 
        encoder = pd.read_csv('/home/milenasilva/Chat_ibict/Progressao/static/Modelos/encoder_CienciasAgrarias.csv')
    
    sub = ''

    sub = prevXGB(entrada, path_model)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(encoder)

    sub = label_encoder.inverse_transform(sub)
    sub = sub[0]

    print(f"""c("{sub}", "{area}")""")


    return f"""c("{sub}", "{area}")"""

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
                    resultado_limpo = re.sub(r'^\w+\(|\)$|\"', '', resultado)
                    partes = resultado_limpo.split(',')
                    subarea = partes[0].strip()
                    area = partes[1].strip()

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
