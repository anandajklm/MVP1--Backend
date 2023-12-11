# Minha API

MVP 1 - Pós Graduação em Engenharia de Software - PUC-Rio 2023

Neste Projeto utilizei Python e Flask para desenvolver as rotas de API e a comunicação com o banco de dados SQLite. Ele consiste na implementação backend de um organizador de gastos para gestão financeira pessoal, onde o cliente poderá registrar seus gastos e classificá-los. Futuramente o projeto pode evoluir com gráficos para insights para gestão financeiras

---
## Como executar 


Para a execução bem-sucedida do projeto, é aconselhável instalar as bibliotecas Python listadas no arquivo requirements.txt, disponível no repositório. Embora não seja obrigatório, recomenda-se realizar essas instalações em um ambiente virtual, como o [virtualenv], para evitar conflitos de versões com outros projetos na máquina. Os comandos a seguir podem ser utilizados para realizar essa etapa, considerando o uso da versão 3.9 do Python:

```
$ python -m venv env
$ .\env\Scripts\activate
```


Em seguida, realizar o download de dependências do projeto com o comando a seguir:

```
(env_app)$ pip install -r requirements.txt
```

Finalmente, para executar a API, basta digitar o comando abaixo: 

```
(env)$ flask run --host 0.0.0.0 --port 5000
```
Se desejar verificar o status da API em execução, é suficiente abrir o seguinte link no navegador: http://localhost:5000/#/

Se desejar encerrar o servidor, pressione Ctrl + C no terminal em execução,que ele será interrompido.

Para sair do ambiente virtual, utilize o comando a seguir:

```
(env_app)$ deactivate
```
