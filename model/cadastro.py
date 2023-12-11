from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Cadastro(Base):
    
    __tablename__ = 'cadastro'
    
    id = Column("pk_cadastro", Integer, primary_key=True) 
    classificacao = Column(String(70))
    valor = Column(Integer)
    data_cadastro = Column(String(10))
    data_insercao = Column(DateTime, default=datetime.now())

    
    def __init__(self, classificacao:str, valor:Integer, data_cadastro:str , data_insercao:Union[DateTime, None] = None):
        
        self.classificacao = classificacao
        self.valor = valor        
        self.data_cadastro = data_cadastro
        
        if data_insercao:
            self.data_insercao = data_insercao