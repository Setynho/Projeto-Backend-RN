from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from .conexao import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Atributos essenciais de privacidade da LGPD
    consentimento_lgpd = Column(Boolean, default=False, nullable=False)
    data_consentimento = Column(DateTime, default=datetime.utcnow)

class Unidade(Base):
    __tablename__ = 'unidades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(50), nullable=False)

class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    categoria = Column(String(50), nullable=False) # Ex: "Tapioca", "Cuscuz", "Bebida"
    eh_sazonal = Column(Boolean, default=False, nullable=False) # Tratamento de pratos juninos

class CardapioLocal(Base):
    __tablename__ = 'cardapios_locais'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidade_id = Column(Integer, ForeignKey('unidades.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    preco_regional = Column(Float, nullable=False)
    em_estoque = Column(Boolean, default=True, nullable=False)