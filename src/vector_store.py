# src/vector_store.py
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
# ATUALIZADO: A importação mudou de langchain.text_splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import config
import os

# Configurações
AMPI_PDF_PATH = os.path.join(config.DOCS_DIRECTORY, "Questionario_AMPI_Adaptado.pdf")
PASTA_BASE = config.DOCS_DIRECTORY

# Embeddings gratuitos
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)  # <--- O ERRO ESTAVA AQUI! FALTAVA ESTE PARÊNTESE.

def create_ampi_guide_db():
    """Cria o banco vetorial com o PDF oficial da AMPI."""
    print(f"Processando o guia oficial AMPI: {AMPI_PDF_PATH}...")
    
    if not os.path.exists(AMPI_PDF_PATH):
        print(f"Erro: Arquivo {AMPI_PDF_PATH} não encontrado.")
        print(f"Verifique se o arquivo 'Questionario_AMPI_Adaptado.pdf' existe dentro da pasta 'base'.")
        return
    loader = PyPDFLoader(AMPI_PDF_PATH)
    pages = loader.load()
    print(f"Guia AMPI carregado com {len(pages)} páginas.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE, 
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(pages)
    print(f"Guia dividido em {len(chunks)} chunks.")
    print("Criando embeddings para o guia AMPI e salvando no ChromaDB...")
    db_guide = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.DB_AMPI_GUIDE_DIRECTORY
    )
    print(f"✅ Banco de dados do guia AMPI criado com sucesso!")

def criar_db():
    """Cria o banco de dados vetorial com todos os PDFs da pasta base."""
    print("Carregando documentos da pasta base...")
    documentos = carregar_documentos()
    if not documentos:
        print("❌ Nenhum documento encontrado na pasta 'base'!")
        return
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    if not os.path.exists(PASTA_BASE):
        print(f"Erro: Pasta '{PASTA_BASE}' não encontrada!")
        return []
    
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    documentos = carregador.load()
    print(f"📄 {len(documentos)} documentos carregados (excluindo o guia AMPI)")
    
    # Filtrar o guia para não processá-lo duas vezes
    documentos_filtrados = [doc for doc in documentos if os.path.basename(doc.metadata.get('source', '')) != "Questionario_AMPI_Adaptado.pdf"]
    print(f"📄 {len(documentos_filtrados)} documentos filtrados para processar.")
    return documentos_filtrados

def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )
    chunks = separador_documentos.split_documents(documentos)
    print(f"📦 {len(chunks)} chunks criados")
    return chunks

def vetorizar_chunks(chunks):
    print("Criando embeddings e salvando no ChromaDB...")
    db = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory=config.DB_PERSIST_DIRECTORY
    )
    print(f"✅ Banco de dados da pasta 'base' criado com sucesso!")

if __name__ == "__main__":
    print("="*60)
    print("🤖 AMPI - Criação de Banco de Dados Vetorial")
    print("="*60)
    
    print("\n=== Criando banco de dados do guia AMPI ===")
    create_ampi_guide_db()
    
    print("\n=== Criando banco de dados da pasta base ===")
    criar_db()
    
    print("\n" + "="*60)
    print("✅ Processo concluído!")
    print("="*60)