# Chat_ibict
  Repositório para versionamento de codigo do sistema Chat Ibict.

## Tecnologias utilizadas
  - Backend: Django
  - Frontend: HTML e CSS
  - banco de dados: Postgrees
 
## Pesquisadores
  - Sérgio Freitas
  - André Corrêa
  - Milena Faria
  - Renan Carneiro

# Getting Started

## Configurando e subindo o ambiente pela primeira vez

Para subir o ambiente corretamente sao necessarias as seguintes ferramentas:

* Python
* R
* Django

### Instalando ferramentas

* Para instalar o Python, recomenda-se seguir o tutorial oficial disponivel [aqui](https://python.org.br/instalacao-linux/).
* Para instalar o R, recomenda-se seguir os passos oficiais disponivel [aqui](https://cran.r-project.org/).
* Para instalar o Django, recomenda-se seguir o tutorial oficial disponivel [aqui](https://www.djangoproject.com/download/).

### Executando servicos

O ambiente depende de algumas bibliotecas especificados no arquivo `requeriments.txt`, portanto navegue ate a pasta `Chat_ibict/requiriments` e execute o comando:

```
pip install -r requirements.txt
```

Apos a instalacao das bibliotecas va para o diretorio `Chat_ibict/Progressao` e execute os seguintes comandos:

```
pip install -U pip setuptools
```
* Instale o PgAdmin [aqui](https://www.pgadmin.org/download/).

Depois de instalado abra o PgAdmin e na pagina inicial clique em Add New Server.

Na janela que abrir na sessao geral de um nome por exemplo: localhost. Va para a sessao connection e no primeiro campo digite localhost e salve.

Agora clique no servidor que voce criou > Databases > testy clique com o botao esquerdo e selecione a opcao restore e restaure as modelos sql presentes no repositorio, depois clique com o botao esquerdo em testy e selecione a opcao refresh.

Depois rode os seguintes comandos:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
