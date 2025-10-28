# src/perguntas_ampi.py

PERGUNTAS_AMPI = [
    {
        "id": 1,
        "categoria": "mobilidade",
        "pergunta": "Você tem dificuldade para caminhar?",
        "opcoes": ["Não", "Pouca dificuldade", "Muita dificuldade"],
        "pesos": {"cardiologia": 1, "ortopedia": 3, "geriatria": 2}
    },
    {
        "id": 2,
        "categoria": "mobilidade",
        "pergunta": "Você sente dores nas articulações?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"ortopedia": 3, "geriatria": 1, "reumatologia": 2}
    },
    {
        "id": 3,
        "categoria": "cognitivo",
        "pergunta": "Você tem esquecido coisas recentes com frequência?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"neurologia": 3, "geriatria": 2, "psiquiatria": 1}
    },
    {
        "id": 4,
        "categoria": "cardiovascular",
        "pergunta": "Você sente falta de ar ao fazer esforços?",
        "opcoes": ["Não", "Em esforços grandes", "Em esforços pequenos"],
        "pesos": {"cardiologia": 3, "pneumologia": 2, "geriatria": 1}
    },
    {
        "id": 5,
        "categoria": "cardiovascular",
        "pergunta": "Você sente dores no peito?",
        "opcoes": ["Não", "Raramente", "Frequentemente"],
        "pesos": {"cardiologia": 4, "geriatria": 1}
    },
    {
        "id": 6,
        "categoria": "nutricional",
        "pergunta": "Como está seu apetite?",
        "opcoes": ["Normal", "Diminuído", "Muito diminuído"],
        "pesos": {"geriatria": 2, "gastroenterologia": 2, "nutricao": 3}
    },
    {
        "id": 7,
        "categoria": "emocional",
        "pergunta": "Você tem se sentido triste ou deprimido?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"psiquiatria": 3, "geriatria": 2}
    },
    {
        "id": 8,
        "categoria": "sono",
        "pergunta": "Você tem dificuldade para dormir?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"neurologia": 2, "psiquiatria": 2, "geriatria": 1}
    },
    {
        "id": 9,
        "categoria": "visao",
        "pergunta": "Você tem dificuldade para enxergar?",
        "opcoes": ["Não", "Um pouco", "Muita dificuldade"],
        "pesos": {"oftalmologia": 3, "geriatria": 1}
    },
    {
        "id": 10,
        "categoria": "audicao",
        "pergunta": "Você tem dificuldade para ouvir?",
        "opcoes": ["Não", "Um pouco", "Muita dificuldade"],
        "pesos": {"otorrinolaringologia": 3, "geriatria": 1}
    },
    {
        "id": 11,
        "categoria": "quedas",
        "pergunta": "Você sofreu alguma queda nos últimos 6 meses?",
        "opcoes": ["Não", "Uma vez", "Mais de uma vez"],
        "pesos": {"ortopedia": 2, "neurologia": 2, "geriatria": 3}
    },
    {
        "id": 12,
        "categoria": "medicamentos",
        "pergunta": "Você toma mais de 5 medicamentos diferentes?",
        "opcoes": ["Não", "Sim"],
        "pesos": {"geriatria": 3, "farmacia_clinica": 2}
    },
    {
        "id": 13,
        "categoria": "urinario",
        "pergunta": "Você tem perda involuntária de urina?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"urologia": 3, "geriatria": 2}
    },
    {
        "id": 14,
        "categoria": "social",
        "pergunta": "Você mora sozinho(a)?",
        "opcoes": ["Não", "Sim"],
        "pesos": {"geriatria": 2, "assistencia_social": 2}
    },
    {
        "id": 15,
        "categoria": "atividades",
        "pergunta": "Você precisa de ajuda para atividades do dia a dia (banho, vestir, comer)?",
        "opcoes": ["Não", "Às vezes", "Sempre"],
        "pesos": {"geriatria": 3, "fisioterapia": 2}
    },
    {
        "id": 16,
        "categoria": "equilibrio",
        "pergunta": "Você sente tontura ou vertigem?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"neurologia": 2, "otorrinolaringologia": 2, "geriatria": 1}
    },
    {
        "id": 17,
        "categoria": "pele",
        "pergunta": "Você tem feridas ou machucados que demoram para cicatrizar?",
        "opcoes": ["Não", "Sim"],
        "pesos": {"dermatologia": 2, "angiologia": 2, "geriatria": 1}
    },
    {
        "id": 18,
        "categoria": "digestivo",
        "pergunta": "Você tem problemas de prisão de ventre?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"gastroenterologia": 2, "geriatria": 1}
    },
    {
        "id": 19,
        "categoria": "temperatura",
        "pergunta": "Você sente muito frio ou muito calor em ambientes normais?",
        "opcoes": ["Não", "Às vezes", "Frequentemente"],
        "pesos": {"endocrinologia": 2, "geriatria": 1}
    },
    {
        "id": 20,
        "categoria": "peso",
        "pergunta": "Você perdeu peso sem fazer dieta nos últimos 6 meses?",
        "opcoes": ["Não", "Pouco peso (menos de 5kg)", "Muito peso (mais de 5kg)"],
        "pesos": {"geriatria": 2, "endocrinologia": 2, "nutricao": 2}
    }
]

def get_perguntas_aleatorias(quantidade=10):
    """Retorna um número aleatório de perguntas da lista"""
    import random
    return random.sample(PERGUNTAS_AMPI, min(quantidade, len(PERGUNTAS_AMPI)))