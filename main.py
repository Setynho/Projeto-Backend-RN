from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.conexao import obter_banco
from database.modelos import CardapioLocal
from pydantic import BaseModel, EmailStr
from database.modelos import Cliente
from pydantic import BaseModel

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


# 1. Modelo de envio para simular o recebimento do pagamento do gateway
class ConfirmacaoPagamento(BaseModel):
    pedido_id: int
    status_transacao: str  # Deve ser 'sucesso' ou 'recusado'

# 2. Endpoint de Simulação do Gateway Desacoplado (Atende ao RF03)
@app.post("/api/v1/pagamentos/webhook")
def processar_webhook_pagamento(dados: ConfirmacaoPagamento):
    # Simulando o recebimento da resposta assíncrona da operadora de cartão
    if dados.status_transacao.lower() == "sucesso":
        # Na lógica real, aqui buscaríamos o pedido no banco SQL e faríamos um UPDATE
        return {
            "status": "Transacao Aprovada",
            "pedido_id": dados.pedido_id,
            "mensagem": "Status do pedido atualizado para 'Pago' com sucesso no banco SQL."
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail=f"Pagamento do pedido {dados.pedido_id} foi recusado pela operadora externa."
        )

