from database.conexao import engine, Base
# Importamos os modelos para que a Base saiba quais tabelas devem ser criadas
from database.modelos import Cliente, Unidade, CardapioLocal

print("Iniciando a criação das tabelas no banco de dados...")

try:
    # Este comando lê tudo o que herdou de Base e cria os objetos correspondentes no banco
    Base.metadata.create_all(bind=engine)
    print("Sucesso! O arquivo de banco de dados 'raizes_nordeste.db' foi gerado.")
except Exception as erro:
    print(f"Ocorreu um erro ao criar o banco de dados: {erro}")