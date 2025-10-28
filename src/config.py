# src/config.py
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env que deve estar na pasta raiz do projeto
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env') # Caminho relativo da src para a raiz
load_dotenv(dotenv_path=dotenv_path)

print(f"Tentando carregar .env de: {dotenv_path}") # Debug
if os.path.exists(dotenv_path):
    print(".env file found by config.py.")
else:
    print("WARNING: .env file NOT found by config.py.")


# --- Configurações da OpenAI e LLM ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Se não carregou do .env, tenta carregar como variável de ambiente do sistema (menos comum)
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("A chave da API da OpenAI (OPENAI_API_KEY) não foi encontrada. Verifique seu arquivo .env na raiz do projeto ou as variáveis de ambiente.")
else:
    print("OPENAI_API_KEY carregada com sucesso pelo config.py.")


LLM_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7

# --- Configurações de Processamento de Documentos ---
# Ajuste DOCS_DIRECTORY para apontar para onde estão seus PDFs (pasta 'base')
DOCS_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'base')
DB_PERSIST_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db') # Cria a pasta 'db' na raiz
DB_AMPI_GUIDE_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', 'db_ampi_guide') # Pasta para o banco de dados do guia AMPI

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- Configurações de Retrieval ---
RETRIEVAL_TOP_K = 5

# --- Configurações do Banco de Dados ---
# <<< ESTA É A LINHA QUE ADICIONAMOS >>>
DATABASE_FILE = os.path.join(os.path.dirname(__file__), '..', 'dados_pacientes.csv')

# --- Senha do Dashboard Admin ---
# (Você pode adicionar esta seção se ainda não tiver)
ADMIN_PASSWORD = "admin123"  # MUDE ISSO para algo mais seguro!

# --- Prompt Template Centralizado ---
PROMPT_TEMPLATE = """Você é o AMPI, um assistente de IA especializado em responder perguntas com base nos documentos fornecidos. 
Use o contexto abaixo para responder à pergunta do usuário de forma clara e precisa.

Contexto:
{context}

Pergunta: {question}

Resposta:"""