# Api Consultas médicas (Appointment) - Projeto MVP

Projeto MVP para disciplina **Desenvolvimento Backend Avançado** 

Este projeto é uma aplicação back-end desenvolvida com Python Utilizando Flask. O objetivo é criar um serviço para interagir com front-end permitindo adicionar, editar, excluir e visualizar informações dos Consultas médicass.


## Funcionalidades

- **Cadastro de Consultas médicas**: Permite adicionar novos Consultas médicass com informações como id do paciente, crm do medico, data do atendimento e sintomas.
- **Alteração de Consultas médicas**: Permite alterar as informações dos Consultas existentes.
- **Busca de Consultas médicas**: Permite buscar as informações dos Consultas existentes para edição.
- **Exclusão de Consultas médicas**: Permite excluir Consultas médicas do banco de dados.
- **Visualização de Consultas médicas**: Lista todos os Consultas filtrando por id do paciente.



## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal utilizada no projeto.
- **Flask**: Framework para desenvolvimento da API.
- **SQLite**: Banco de dados utilizado para armazenar os dados dos Consultas médicass e endereços.
- **Pydantic**: Biblioteca para validação de dados e definição de esquemas.
- **flask-openapi3**: Biblioteca para documentação da API.



## Criar a Chave do Gemini para usar a api.

Antes de tudo, vamos precisar criar uma Api Key no Google Cloud. Esta
Api key é necessária para rodar a api que busca a sugestão de remédios
conforme os sintomas do paciente é informado.

Acesse a url abaixo para criar a chave:

```
https://aistudio.google.com/apikey
```

Clique no botão "Criar Chave de Api"

Ao criar, copie a chave criada para ser usada na variavel GEMINI_TOKEN
onde mostraremos onde inserir, a seguir.

Importante: Não compartilhe essa chave com ninguém:

## Instalando o projeto

Será necessário ter o python instalado. A versão indicada é a 3.12.6 e a do pip é a 24.2. 
Após clonar o repositório, é necessário ir ao diretório raiz do projeto, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Instale o venv:

```
 python -m venv .venv 
```

Ative o Venv com o comando abaixo:

```
 .venv\Scripts\activate
```

Assim que ativado, instale as depedencias.

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Crie um arquivo .env e coloque o o conteúdo:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
GEMINI_AI_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
GEMINI_TOKEN=<TOKEN DO GEMINI GERADA>
```
## Rodando a aplicação

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 4000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 4000 --reload
```

## Rodando Testes

Esta aplicação possui testes unitários. Para rodar os testes, basta instalar
o projeto e em seguida executar o comando abaixo:

```
(env)$ pytest
```

Observação: Esta aplicaçao precisa do mysql rodando para o teste, pois o 
pytest também executa teste de conexão com banco de dados.

## Rodando via Docker (Precisa ter o Docker Instalado)

Rodando via docker-compose

Para criar o banco de dados mysql, execute o comando abaixo:

```
docker-compose up
```

Execute o comando para gerar a imagem via Docker

```
docker build -t api--appointment .
```

Para executar o container, rode o comando abaixo:

```
docker run --name api--appointment \
    --network api-backend \  
    -p 4000:5000 \
    -e DB_PASSWORD=<SENHA DO BANCO> \
    -e DB_USER=<USUARIO DE BANCO> \
    -e DB_HOST=<IP DO BANCO> \ 
    -e DB_PORT=<PORTA DO BANCO> \ 
    -e GEMINI_AI_URL=<URL DO GEMINI> \
    -e GEMINI_TOKEN=<TOKEN DO GEMINI> \
    api--appointment:latest
```

## Documentação OpenAPI

A documentação OpenAPI da API está disponível em:

- **URL**: `[http://localhost:4000/openapi/swagger](http://localhost:4000/openapi/swagger)`


## POSTMAN

Para executar, importe as collections do postman 

```
api--appointment.postman_collection.json
```

## Autor
Clayton Morais de Oliveira
