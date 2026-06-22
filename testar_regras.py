from database.conexao import obter_banco
from database.modelos import Cliente

# Abre a sessão do banco de dados usando o nosso gerenciador
banco_gerenciador = obter_banco()
banco = next(banco_gerenciador)

print("\n--- Iniciando testes de regras de negócio ---")

try:
    # Criando um cliente que aceitou os termos da LGPD (Cenário Válido)
    novo_cliente_valido = Cliente(
        nome="Ruan Silva",
        email="ruan@email.com",
        consentimento_lgpd=True
    )
    
    # Adiciona e salva no banco SQL
    banco.add(novo_cliente_valido)
    banco.commit()
    print(f"Sucesso: Cliente '{novo_cliente_valido.nome}' inserido com consentimento LGPD.")

    # Fazendo um SELECT (Busca) para comprovar a gravação
    cliente_salvo = banco.query(Cliente).filter_by(email="ruan@email.com").first()
    print(f"Verificação no Banco -> ID: {cliente_salvo.id} | LGPD Aceito: {cliente_salvo.consentimento_lgpd}")

except Exception as erro:
    banco.rollback() # Cancela a operação em caso de erro
    print(f"Erro ao processar operações no banco: {erro}")

finally:
    # Fecha a conexão com o banco com segurança
    next(banco_gerenciador, None)
    print("Conexão com o banco de dados fechada com segurança.\n")