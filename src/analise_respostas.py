# src/analise_respostas.py

def analisar_respostas(perguntas_respondidas, respostas):
    """
    Analisa as respostas e retorna especialidade recomendada
    
    Args:
        perguntas_respondidas: Lista de perguntas que foram feitas
        respostas: Dicionário com as respostas {id_pergunta: resposta_escolhida}
    
    Returns:
        dict com especialidade, urgencia e detalhes
    """
    scores = {}
    detalhes_categorias = {}
    
    for pergunta in perguntas_respondidas:
        pergunta_id = pergunta['id']
        resposta = respostas.get(pergunta_id, "")
        
        # Contar categorias
        categoria = pergunta['categoria']
        if categoria not in detalhes_categorias:
            detalhes_categorias[categoria] = 0
        
        # Calcular pontos baseado na resposta
        indice_resposta = pergunta['opcoes'].index(resposta) if resposta in pergunta['opcoes'] else 0
        
        # Somar pontos para cada especialidade
        for especialidade, peso in pergunta['pesos'].items():
            if especialidade not in scores:
                scores[especialidade] = 0
            
            # Quanto pior a resposta, mais pontos (indice maior = mais grave)
            scores[especialidade] += peso * indice_resposta
        
        # Contar problemas por categoria
        if indice_resposta > 0:  # Se não for "Não" ou a primeira opção
            detalhes_categorias[categoria] += 1
    
    # Encontrar especialidade com maior pontuação
    if not scores:
        return {
            'especialidade': 'geriatria',
            'urgencia': 'baixa',
            'scores': {},
            'categorias_problema': [],
            'recomendacao': 'Consulta de rotina recomendada'
        }
    
    especialidade_principal = max(scores, key=scores.get)
    pontuacao_maxima = scores[especialidade_principal]
    
    # Determinar urgência baseada na pontuação
    if pontuacao_maxima >= 15:
        urgencia = 'alta'
        recomendacao = 'Recomendamos agendar consulta o mais breve possível'
    elif pontuacao_maxima >= 8:
        urgencia = 'média'
        recomendacao = 'Recomendamos agendar consulta nas próximas semanas'
    else:
        urgencia = 'baixa'
        recomendacao = 'Consulta de acompanhamento recomendada'
    
    # Categorias com problemas
    categorias_problema = [cat for cat, count in detalhes_categorias.items() if count > 0]
    
    # Top 3 especialidades
    top_especialidades = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        'especialidade': especialidade_principal,
        'urgencia': urgencia,
        'scores': dict(top_especialidades),
        'categorias_problema': categorias_problema,
        'recomendacao': recomendacao,
        'pontuacao_total': pontuacao_maxima
    }


def formatar_nome_especialidade(especialidade):
    """Formata o nome da especialidade para exibição"""
    nomes = {
        'cardiologia': 'Cardiologia',
        'ortopedia': 'Ortopedia',
        'neurologia': 'Neurologia',
        'geriatria': 'Geriatria',
        'psiquiatria': 'Psiquiatria',
        'reumatologia': 'Reumatologia',
        'pneumologia': 'Pneumologia',
        'gastroenterologia': 'Gastroenterologia',
        'nutricao': 'Nutrição',
        'oftalmologia': 'Oftalmologia',
        'otorrinolaringologia': 'Otorrinolaringologia',
        'urologia': 'Urologia',
        'assistencia_social': 'Assistência Social',
        'fisioterapia': 'Fisioterapia',
        'dermatologia': 'Dermatologia',
        'angiologia': 'Angiologia',
        'endocrinologia': 'Endocrinologia',
        'farmacia_clinica': 'Farmácia Clínica'
    }
    return nomes.get(especialidade, especialidade.capitalize())