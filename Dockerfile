# define a imagem base
FROM python:3.9-alpine

# evita que a saída do python no terminal seja bufferizada
ENV PYTHONUNBUFFERED 1

# cria o diretório de trabalho
WORKDIR /code

# as instruções ADD, COPY, CMD, ENTRYPOINT ou RUN serão executadas no diretório de trabalho definido anteriormente

# copia os arquivos utilizados na instalação de dependências para o diretório de trabalho
COPY ./requirements /code/requirements/

# atualiza o pip e instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements/dev-requirements.txt
RUN python3 -m spacy download pt_core_news_lg

# copia o restante do projeto para o diretório de trabalho
COPY . /code/
