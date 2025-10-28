Projeto-4-semestre-AMPI RASCUNHO
AMPI-PREDICT: Classificação de Risco Geriátrico Turma: X | Curso: [Nome do Curso] | Período: Noturno | Ano: 2025

Equipe e Papéis Integrante RA Papel principal Principais entregas (commits/arquivos) [Seu Nome] [Seu RA] Líder, Gerência e Integração/UX src/main.py, README.md (Revisão), Gestão do GitHub [Membro 1] [RA do M1] Engenharia de Dados src/data_prep.py, data/raw/* [Membro 2] [RA do M2] Modelagem src/train.py, models/knn_model.pkl [Membro 3] [RA do M3] Avaliação & Gráficos src/evaluate.py, reports/figures/* [Membro 4] [RA do M4] Documentação & Vídeo docs/ARCHITECTURE.md, Roteiro do Vídeo

Exportar para as Planilhas Todos devem ter mínimo 2 commits.

Problema O Brasil possui uma população idosa crescente, exigindo estratégias eficientes de saúde preventiva. O AMPI-Predict aborda a dificuldade de triagem rápida, que classifica o idoso em uma das três categorias de risco (Baixo, Moderado, Alto) com base em 17 domínios geriátricos (escore AMPI). Nosso objetivo é automatizar essa classificação com uma precisão confiável, garantindo que idosos de alto risco sejam rapidamente identificados para intervenção. O sistema funciona se a IA for capaz de diferenciar as três classes e minimizar drasticamente os Falsos Negativos (idosos de alto risco classificados erroneamente como baixo).
Métrica(s) alvo:

Principal: F1-Score (Weighted) — Essencial para equilibrar Precisão e Recall em classes potencialmente desbalanceadas, priorizando a segurança clínica.

Secundária: Acurácia (Accuracy) — Mede a proporção geral de acertos do modelo.

Abordagem de IA Tipo de IA/ML: Classificação Supervisionada Multiclasse.
Justificativa técnica: O problema é categórico (classes discretas: Baixo, Moderado, Alto). Utilizamos o K-Nearest Neighbors (KNN), conforme estudado na Aula 7, por sua simplicidade e eficácia em problemas baseados em distância. A padronização dos dados (StandardScaler) é crucial para que o KNN funcione corretamente.

Semente aleatória: 42 (Usada em train_test_split para garantir a reprodutibilidade).

Dados Origem: Fictício. Os dados foram gerados via NumPy e Pandas (src/data_prep.py), simulando 17 pontuações de 0 a 2 (seguindo a estrutura do AMPI) e a criação da coluna de risco com base na pontuação total.
Esquema:

Features (X): 17 colunas (Idade, Mobilidade, Cognicao, Suporte_Social, etc. — tipo: Numérico, int).

Target (y): 1 coluna (Nivel_de_Risco — tipo: Categórico, valores: 'Baixo', 'Moderado', 'Alto').

Cuidados éticos/privacidade: Por serem dados fictícios, não há questões de privacidade. Em um cenário real, dados de saúde exigiriam anonimização total.

Tamanho aproximado: 1000 linhas × 17 colunas.

Importante: O script src/data_prep.py gera e salva os dados; não é necessário baixar. Detalhes estão em data/README_DATA.md.

Estrutura do Projeto PROJ_IA_2025_TurmaX_GrupoYY/ ├─ README.md ├─ requirements.txt ├─ src/ │ ├─ config.py (Variáveis como RANDOM_STATE) │ ├─ data_prep.py (Geração e Padronização - Membro 1) │ ├─ train.py (Treino do Modelo e salvamento - Membro 2) │ ├─ evaluate.py (Cálculo de Métricas/Gráficos - Membro 3) │ └─ main.py (Interface Streamlit/Integração - Líder/Dev) ├─ notebooks/ ├─ data/ ├─ models/ (knn_model.pkl, scaler.pkl) ├─ reports/ └─ docs/ (ARCHITECTURE.md)
Como Reproduzir 5.1 Ambiente Siga os passos abaixo para preparar o ambiente virtual e instalar as dependências (Pandas, Scikit-learn, Streamlit, Matplotlib).
Bash

python -m venv .venv

Windows: .venv\Scripts\activate
Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt 5.2 Treinamento e Execução Execute os módulos na ordem para gerar os dados, treinar a IA e rodar o aplicativo de demonstração:

Bash

1. Preparação de Dados (Membro 1)
python src/data_prep.py

2. Treinamento da IA (Membro 2)
python src/train.py

3. Avaliação (Membro 3)
python src/evaluate.py

4. Execução da Interface (Líder/Dev)
Isto abrirá o aplicativo web no seu navegador.
streamlit run src/main.py 6. Resultados Métricas (tabela curta):

Métrica	Valor (Exemplo)
Acurácia	[Ex: 0.88]
F1-Score (Weighted)	[Ex: 0.87]
Recall (Alto Risco)	[Ex: 0.91]
Gráficos (imagens): (Incluir imagens da Matriz de Confusão, Distribuição do Target, e Comparação de k vs. F1-Score)

Interpretação:

Matriz de Confusão: [Ex: A matriz mostra que a maioria dos erros (Falsos Negativos) ocorre ao classificar o "Moderado" como "Baixo", mas o erro crítico (Alto Risco como Baixo) é minimizado, validando a alta pontuação de Recall.]

Comparação k vs. F1-Score: [Ex: O gráfico de linha confirma que o k=5 (ou 7) foi o ideal, pois ofereceu o pico de F1-Score, justificando a escolha do hiperparâmetro.]

Decisões Técnicas Pré-processamento:
Geração do Target: Usamos limites de pontuação (ex: 0-10=Baixo, 11-20=Moderado, 21-34=Alto) para criar as classes, transformando o problema em Classificação Multiclasse.

Normalização: Utilizado StandardScaler em todas as 17 features. Isso garante que a distância Euclidiana (base do KNN) não seja dominada por nenhuma variável, padronizando a média em 0 e o desvio em 1.

Arquitetura/Hiperparâmetros:

Algoritmo: K-Nearest Neighbors (KNN).

Parâmetro: k=5 (definido após a otimização pelo Membro 3).

Treino: Divisão de 70/30 com train_test_split(..., random_state=42).

Limitações Conhecidas e Possíveis Melhorias:

Limitação: A base de dados é fictícia, o que pode não refletir nuances clínicas reais.

Melhoria: Testar outros modelos (como Random Forest, citado na Aula 7) e implementar a otimização de hiperparâmetros via GridSearch para encontrar o melhor k.

Execução do Vídeo (YouTube) Link: [colar o link do YouTube aqui]
Roteiro seguido: Problema (M4) → Dados (M1) → IA e Treinamento (M2) → Resultados (M3) → Execução ao Vivo na Interface Streamlit (Líder/Dev) → Conclusão (M4).

Créditos e Licença Autores: [Nomes e RAs de todos os 5 membros]
Licença escolhida: MIT (Padrão para projetos acadêmicos e open source).

Changelog (opcional) v1.0 — Entrega final do projeto de Classificação (KNN).
v0.9 — Ajuste fino da avaliação e gráficos.
