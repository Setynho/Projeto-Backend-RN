from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define onde o banco de dados será criado (arquivo raizes_nordeste.db)
URL_BANCO = "sqlite:///./raizes_nordeste.db"

# 2. Cria o motor de conexão do banco de dados
engine = create_engine(
    URL_BANCO, 
    connect_args={"check_same_thread": False}  # Necessário para o SQLite funcionar com APIs
)

# 3. Cria a fábrica de sessões (usada para fazer inserts, updates e selects)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Classe base que todas as nossas tabelas vão herdar
Base = declarative_base()

# Função utilitária para abrir e fechar a conexão com o banco de forma segura
def obter_banco():
    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()
