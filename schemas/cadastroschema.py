from pydantic import BaseModel
from typing import Optional, List
from model.cadastro import Cadastro

class CadastroSchema(BaseModel):
    """ Define como um novo cadastro ser inserido deve ser representado
    """
    classificacao: str = "Mercado"
    valor: int = 100
    data_cadastro: str = "07/12/2023"
    
class CadastroViewSchema(BaseModel):
    """ Define como um cadastro será retornado: cadastro + comentários.
    """
    id: int = 1
    classificacao: str = "Mercado"
    valor: int = 101
    data_cadastro : str = "07/12/2023"

def apresenta_cadastro(cadastro: Cadastro):
    """ Retorna uma representação do cadastro seguindo o schema definido em
        CadastroViewSchema.
    """
    return {
        "id": cadastro.id,
        "classificacao": cadastro.classificacao,
        "valor": cadastro.valor,
        "data_cadastro": cadastro.data_cadastro
    }
    
class CadastroBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por um cadastro. 
        Deverão ser fornecidos a classificacao e a data do cadastro
    """
    classificacao: str = "Conta de Luz"
    data_cadastro: str = "07/12/2023"


class ListagemCadastrosSchema(BaseModel):
    """ Define como uma listagem de cadastros será retornada.
    """
    veiculos:List[CadastroSchema]
    

def apresenta_cadastros(cadastros: List[Cadastro]):
    """ Retorna uma representação do cadastro seguindo o schema definido em
        CadastroViewSchema.
    """
    result = []
    for cadastro in cadastros:
        result.append({
            "classificacao": cadastro.classificacao,
            "valor": cadastro.valor,
            "data_cadastro": cadastro.data_cadastro
        })

    return {"cadastros": result}


class CadastroDelSchema(BaseModel):
    """ Define como uma listagem de cadastros será retornada.
    """
    classificacao: str
    data_cadastro: str