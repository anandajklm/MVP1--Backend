from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session
from model.cadastro import Cadastro
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cadastro_tag = Tag(name="Cadastro", description="Adição, visualização e remoção de cadastros financeiros")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cadastro', tags=[cadastro_tag],
          responses={"200": CadastroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cadastro(form: CadastroSchema):
    """Adiciona um novo cadastro de gasto à base de dados

    Retorna uma representação dos cadastros, com detalhes.
    """
    cadastro = Cadastro(
        classificacao=form.classificacao,
        valor=form.valor,
        data_cadastro=form.data_cadastro
        )
    
    logger.debug(f"Adicionando cadastro '{cadastro.classificacao}' do dia '{cadastro.data_cadastro}'")
    
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cadastro de viagem
        session.add(cadastro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cadastro '{cadastro.classificacao}' do dia '{cadastro.data_cadastro}'")
        return apresenta_cadastro(cadastro), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(e)
        logger.warning(f"Erro ao adicionar cadastro '{cadastro.classificacao}' do dia '{cadastro.data_cadastro}, {error_msg}")
        return {"mesage": error_msg}, 400
    '''
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cadastro de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cadastro '{cadastro.data_cadastro}', {error_msg}")
        return {"mesage": error_msg}, 409
    '''


@app.get('/cadastros', tags=[cadastro_tag],
         responses={"200": ListagemCadastrosSchema, "404": ErrorSchema})
def cadastros():
    """Faz a busca por todos os cadastros na base de dados

    Retorna uma representação da listagem dos cadastros e todas as suas informações.
    """
    logger.debug(f"Capturando cadastros da base de dados...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cadastros  = session.query(Cadastro).all()
    print(len(cadastros))    
    if not cadastros :
        # se não há cadastros
        return {"cadastros ": []}, 200
    else:
        logger.debug(f"%d cadastros  encontrados" % len(cadastros ))
        # retorna a representação de cadastro
        
        return apresenta_cadastros (cadastros ), 200

@app.get('/cadastro', tags=[cadastro_tag],
         responses={"200": CadastroViewSchema, "404": ErrorSchema})
def get_cadastro(query: CadastroBuscaSchema):
   
    """Faz a busca por um Cadastro a partir da classificação e Data.
    Retorna uma representação dos cadastros e detalhes.
    """

    classificacao = query.classificacao
    data_cadastro = query.data_cadastro
    
    logger.debug(f"Coletando dados sobre {classificacao} do dia {data_cadastro}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cadastro = session.query(Cadastro).filter(Cadastro.classificacao == classificacao and Cadastro.data_cadastro == data_cadastro).first()

    if not cadastro:
        # se o cadastro não foi encontrado
        error_msg = "Cadastro não encontrado na base :/"
        logger.warning(f"Erro ao encontrar cadastro {classificacao} do dia {data_cadastro}, {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Cadastro encontrado!")
        # retorna a representação de cadastro
        return apresenta_cadastro(cadastro), 200

@app.delete('/cadastro', tags=[cadastro_tag],
            responses={"200": CadastroDelSchema, "404": ErrorSchema})
def del_cadastro(query: CadastroBuscaSchema):
    """Deleta um Cadastro a partir da classificacao e data informados

    Retorna uma mensagem de confirmação da remoção.
    """
    print(query)
    classificacao_cadastro = query.classificacao
    data_cadastro = unquote(unquote(query.data_cadastro))
    
    print(classificacao_cadastro)
    print(data_cadastro)
    
    logger.debug(f"Deletando dados do cadsatro #{data_cadastro}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cadastro).filter(Cadastro.data_cadastro == data_cadastro and Cadastro.classificacao == classificacao_cadastro).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cadastro {classificacao_cadastro} do dia {data_cadastro}")
        return {"mesage": "Cadastro removido"}, 200
    else:
        # se cadastro não foi encontrado
        error_msg = "Cadastro não encontrado na base."
        logger.warning(f"Erro ao deletar cadastro '{classificacao_cadastro}' do dia '{data_cadastro}', {error_msg}")
        return {"mesage": error_msg}, 404