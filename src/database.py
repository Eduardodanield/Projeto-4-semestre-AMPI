# src/database.py
import pandas as pd
import os
from datetime import datetime
import config

def salvar_paciente(dados_pessoais, respostas, analise):
    """
    Salva os dados do paciente no CSV
    """
    # Preparar registro
    registro = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'nome': dados_pessoais.get('nome', ''),
        'idade': dados_pessoais.get('idade', 0),
        'cidade': dados_pessoais.get('cidade', ''),
        'filhos': dados_pessoais.get('filhos', 0),
        'especialidade_recomendada': analise['especialidade'],
        'urgencia': analise['urgencia'],
        'pontuacao_total': analise['pontuacao_total'],
        'categorias_problema': ', '.join(analise['categorias_problema']),
        'recomendacao': analise['recomendacao']
    }
    
    # Adicionar respostas individuais
    for id_pergunta, resposta in respostas.items():
        registro[f'pergunta_{id_pergunta}'] = resposta
    
    # Salvar no CSV
    arquivo = config.DATABASE_FILE
    
    try:
        if os.path.exists(arquivo):
            df = pd.read_csv(arquivo)
            df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
        else:
            df = pd.DataFrame([registro])
        
        df.to_csv(arquivo, index=False)
        return True, df
    except Exception as e:
        return False, str(e)


def carregar_dados():
    """Carrega todos os dados do CSV"""
    arquivo = config.DATABASE_FILE
    
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    else:
        return pd.DataFrame()


def get_estatisticas():
    """Retorna estatísticas gerais"""
    df = carregar_dados()
    
    if df.empty:
        return {
            'total_pacientes': 0,
            'idade_media': 0,
            'atendimentos_hoje': 0
        }
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    return {
        'total_pacientes': len(df),
        'idade_media': df['idade'].mean() if 'idade' in df.columns else 0,
        'atendimentos_hoje': len(df[df['timestamp'].str.contains(hoje)]) if 'timestamp' in df.columns else 0
    }