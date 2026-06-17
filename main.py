from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.conexao import obter_banco
from database.modelos import CardapioLocal
from pydantic import BaseModel, EmailStr
from database.modelos import Cliente

# Inicializa a aplicação FastAPI
app = FastAPI(title="API Rede Raízes do Nordeste", version="1.0.0")

# 1. Rota de Boas-Vindas (Status do Sistema)
@app.get("/")
def ler_raiz():
    return {"status": "Online", "empresa": "Rede Raízes do Nordeste - Ecossistema Digital"}

# 2. Rota para Listar o Cardápio de uma Unidade (Atende ao RF01 e RNF02)
@app.get("/api/v1/unidades/{unidade_id}/cardapio")
def listar_cardapio_unidade(unidade_id: int, banco: Session = Depends(obter_banco)):
    # Faz uma busca no banco SQL filtrando pela unidade informada na URL
    itens_cardapio = banco.query(CardapioLocal).filter(CardapioLocal.unidade_id == unidade_id).all()
    
    if not itens_cardapio:
        raise HTTPException(status_code=404, detail="Nenhum produto cadastrado ou unidade não encontrada.")
    
    return itens_cardapio
class ClienteCadastro(BaseModel):
    nome: str
    email: str
    consentimento_lgpd: bool

# 2. Rota para Cadastrar Cliente (Atende ao RF02)
@app.post("/api/v1/clientes", status_code=201)
def cadastrar_cliente(cliente_dados: ClienteCadastro, banco: Session = Depends(obter_banco)):
    
    # Validação da LGPD: Se não houver consentimento, o sistema barra o cadastro
    if not cliente_dados.consentimento_lgpd:
        raise HTTPException(
            status_code=400, 
            detail="Cadastro recusado. E obrigatório aceitar os termos de privacidade (LGPD)."
        )
        
    # Verifica se o e-mail já está cadastrado para evitar duplicidade
    email_existente = banco.query(Cliente).filter(Cliente.email == cliente_dados.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="Este e-mail ja esta cadastrado no sistema.")
        
    # Se passou pelas validações, cria o objeto e salva no banco SQL
    novo_cliente = Cliente(
        nome=cliente_dados.nome,
        email=cliente_dados.email,
        consentimento_lgpd=cliente_dados.consentimento_lgpd
    )
    
    banco.add(novo_cliente)
    banco.commit()
    banco.refresh(novo_cliente)
    
    return {"mensagem": "Cliente cadastrado com sucesso!", "id_cliente": novo_cliente.id}