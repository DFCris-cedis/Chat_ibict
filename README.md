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
 Getting Started

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
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
