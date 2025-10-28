# src/main.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import config
from perguntas_ampi import PERGUNTAS_AMPI, get_perguntas_aleatorias
from analise_respostas import analisar_respostas, formatar_nome_especialidade
from database import salvar_paciente, carregar_dados, get_estatisticas

# Configuração da página
st.set_page_config(
    page_title="AMPI-Predict",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Função principal"""
    
    # Sidebar - Menu de navegação
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/doctor-male--v1.png", width=100)
        st.title("Menu")
        
        pagina = st.radio(
            "Navegação:",
            ["🏠 Início", "📝 Questionário", "📊 Dashboard Admin"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Sobre o AMPI-Predict")
        st.info("Sistema inteligente de avaliação geriátrica para identificação de riscos e encaminhamento médico adequado.")
    
    # Roteamento de páginas
    if pagina == "🏠 Início":
        pagina_inicio()
    elif pagina == "📝 Questionário":
        pagina_questionario()
    elif pagina == "📊 Dashboard Admin":
        pagina_dashboard()


def pagina_inicio():
    """Página inicial com boas-vindas"""
    st.markdown('<h1 class="main-header">🤖 AMPI-Predict</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Sistema de Avaliação de Risco Geriátrico Inteligente</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🎯 Objetivo\nAvaliar riscos de saúde em idosos")
    with col2:
        st.success("### 📋 Método\nQuestionário adaptativo inteligente")
    with col3:
        st.warning("### 🏥 Resultado\nEncaminhamento médico personalizado")
    
    st.markdown("---")
    
    st.markdown('<h2 class="sub-header">Como funciona?</h2>', unsafe_allow_html=True)
    
    st.write("""
    1. **Cadastro**: Informe seus dados pessoais
    2. **Questionário**: Responda 10 perguntas selecionadas aleatoriamente
    3. **Análise**: Sistema avalia suas respostas
    4. **Recomendação**: Receba indicação de especialidade médica e locais de atendimento
    """)
    
    if st.button("🚀 Começar Avaliação", type="primary", use_container_width=True):
        st.session_state.etapa = 'dados_pessoais'
        st.rerun()


def pagina_questionario():
    """Página do questionário"""
    
    # Inicializar session_state
    if 'etapa' not in st.session_state:
        st.session_state.etapa = 'dados_pessoais'
    
    if st.session_state.etapa == 'dados_pessoais':
        coletar_dados_pessoais()
    elif st.session_state.etapa == 'perguntas':
        realizar_questionario()
    elif st.session_state.etapa == 'resultado':
        mostrar_resultado()


def coletar_dados_pessoais():
    """Coleta dados pessoais do paciente"""
    st.markdown('<h2 class="sub-header">📋 Dados Pessoais</h2>', unsafe_allow_html=True)
    
    with st.form("form_dados_pessoais"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("👤 Nome completo:", placeholder="Digite seu nome")
            idade = st.number_input("🎂 Idade:", min_value=60, max_value=120, value=65)
        
        with col2:
            cidade = st.text_input("📍 Cidade:", placeholder="Sua cidade")
            filhos = st.number_input("👨‍👩‍👧‍👦 Quantos filhos você tem?", min_value=0, max_value=20, value=0)
        
        submitted = st.form_submit_button("Continuar ➡️", use_container_width=True, type="primary")
        
        if submitted:
            if nome and cidade:
                st.session_state.dados_pessoais = {
                    'nome': nome,
                    'idade': idade,
                    'cidade': cidade,
                    'filhos': filhos
                }
                st.session_state.etapa = 'perguntas'
                st.session_state.perguntas_selecionadas = get_perguntas_aleatorias(10)
                st.session_state.respostas = {}
                st.session_state.pergunta_atual = 0
                st.rerun()
            else:
                st.error("Por favor, preencha todos os campos obrigatórios!")


def realizar_questionario():
    """Realiza o questionário com perguntas aleatórias"""
    st.markdown('<h2 class="sub-header">📝 Questionário AMPI</h2>', unsafe_allow_html=True)
    
    perguntas = st.session_state.perguntas_selecionadas
    pergunta_atual = st.session_state.pergunta_atual
    
    # Barra de progresso
    progresso = (pergunta_atual / len(perguntas)) * 100
    st.progress(progresso / 100)
    st.write(f"Pergunta {pergunta_atual + 1} de {len(perguntas)}")
    
    if pergunta_atual < len(perguntas):
        pergunta = perguntas[pergunta_atual]
        
        st.markdown(f"### {pergunta['pergunta']}")
        
        # Radio button para resposta
        resposta = st.radio(
            "Selecione uma opção:",
            pergunta['opcoes'],
            key=f"pergunta_{pergunta['id']}",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if pergunta_atual > 0:
                if st.button("⬅️ Anterior"):
                    st.session_state.pergunta_atual -= 1
                    st.rerun()
        
        with col3:
            if st.button("Próxima ➡️", type="primary"):
                st.session_state.respostas[pergunta['id']] = resposta
                st.session_state.pergunta_atual += 1
                st.rerun()
    
    else:
        # Todas as perguntas respondidas
        st.success("✅ Questionário concluído!")
        
        if st.button("Ver Resultado 📊", type="primary", use_container_width=True):
            # Analisar respostas
            analise = analisar_respostas(
                st.session_state.perguntas_selecionadas,
                st.session_state.respostas
            )
            st.session_state.analise = analise
            
            # Salvar no banco de dados
            sucesso, resultado = salvar_paciente(
                st.session_state.dados_pessoais,
                st.session_state.respostas,
                analise
            )
            
            if sucesso:
                st.session_state.etapa = 'resultado'
                st.rerun()
            else:
                st.error(f"Erro ao salvar dados: {resultado}")


def mostrar_resultado():
    """Mostra o resultado da avaliação"""
    st.markdown('<h2 class="sub-header">📊 Resultado da Avaliação</h2>', unsafe_allow_html=True)
    
    dados = st.session_state.dados_pessoais
    analise = st.session_state.analise
    
    # Saudação personalizada
    st.markdown(f"### Olá, {dados['nome']}! 👋")
    
    # Card de resultado
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Especialidade Recomendada", 
                 formatar_nome_especialidade(analise['especialidade']))
    
    with col2:
        urgencia_emoji = {"alta": "🔴", "média": "🟡", "baixa": "🟢"}
        st.metric("Nível de Urgência", 
                 f"{urgencia_emoji.get(analise['urgencia'], '🟢')} {analise['urgencia'].capitalize()}")
    
    with col3:
        st.metric("Pontuação Total", analise['pontuacao_total'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recomendação
    st.info(f"💡 **Recomendação:** {analise['recomendacao']}")
    
    # Categorias com problema
    if analise['categorias_problema']:
        st.warning(f"⚠️ **Áreas que requerem atenção:** {', '.join(analise['categorias_problema'])}")
    
    # Top 3 especialidades
    st.markdown("### 📈 Análise Detalhada")
    
    if analise['scores']:
        df_scores = pd.DataFrame(list(analise['scores'].items()), 
                                columns=['Especialidade', 'Pontuação'])
        df_scores['Especialidade'] = df_scores['Especialidade'].apply(formatar_nome_especialidade)
        
        fig = px.bar(df_scores, x='Pontuação', y='Especialidade', 
                    orientation='h',
                    title='Top Especialidades Recomendadas',
                    color='Pontuação',
                    color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    # Locais de atendimento (simulado)
    st.markdown("### 🏥 Locais de Atendimento Próximos")
    st.write(f"📍 Buscando especialistas em **{formatar_nome_especialidade(analise['especialidade'])}** em **{dados['cidade']}**...")
    
    # Simulação de locais
    locais = [
        {"nome": f"Hospital Municipal de {dados['cidade']}", "distancia": "1.2 km", "telefone": "(11) 1234-5678"},
        {"nome": f"UBS {dados['cidade']} Central", "distancia": "2.5 km", "telefone": "(11) 8765-4321"},
        {"nome": f"Clínica Geriátrica {dados['cidade']}", "distancia": "3.8 km", "telefone": "(11) 5555-9999"}
    ]
    
    for local in locais:
        with st.expander(f"📍 {local['nome']} - {local['distancia']}"):
            st.write(f"**Telefone:** {local['telefone']}")
            st.write(f"**Distância:** {local['distancia']}")
            if st.button(f"Ver no Mapa", key=f"mapa_{local['nome']}"):
                st.info("🗺️ Abrindo Google Maps... (funcionalidade a implementar)")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Baixar Relatório PDF", use_container_width=True):
            st.info("Funcionalidade de PDF será implementada em breve!")
    
    with col2:
        if st.button("🔄 Nova Avaliação", use_container_width=True, type="primary"):
            # Limpar session_state
            for key in ['etapa', 'dados_pessoais', 'perguntas_selecionadas', 
                       'respostas', 'pergunta_atual', 'analise']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


def pagina_dashboard():
    """Dashboard administrativo com estatísticas"""
    st.markdown('<h2 class="sub-header">📊 Dashboard Administrativo</h2>', unsafe_allow_html=True)
    
    # Verificar senha
    if 'admin_autenticado' not in st.session_state:
        st.session_state.admin_autenticado = False
    
    if not st.session_state.admin_autenticado:
        senha = st.text_input("🔐 Senha de Administrador:", type="password")
        
        if st.button("Entrar", type="primary"):
            if senha == config.ADMIN_PASSWORD:
                st.session_state.admin_autenticado = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta!")
        
        st.warning("⚠️ Acesso restrito apenas para administradores")
        return
    
    # Dashboard autenticado
    st.success("✅ Autenticado com sucesso!")
    
    if st.button("🚪 Sair"):
        st.session_state.admin_autenticado = False
        st.rerun()
    
    # Carregar dados
    df = carregar_dados()
    
    if df.empty:
        st.warning("📭 Nenhum dado disponível ainda. Aguardando primeiros atendimentos...")
        return
    
    # Estatísticas gerais
    st.markdown("### 📈 Estatísticas Gerais")
    
    stats = get_estatisticas()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total de Pacientes", stats['total_pacientes'])
    
    with col2:
        st.metric("📅 Atendimentos Hoje", stats['atendimentos_hoje'])
    
    with col3:
        st.metric("🎂 Idade Média", f"{stats['idade_media']:.1f} anos")
    
    with col4:
        # Calcular urgências altas
        if 'urgencia' in df.columns:
            urgencias_altas = len(df[df['urgencia'] == 'alta'])
            st.metric("🔴 Urgências Altas", urgencias_altas)
    
    st.markdown("---")
    
    # Abas para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Gráficos", "📋 Dados Detalhados", "📥 Exportar", "⚙️ Configurações"])
    
    with tab1:
        mostrar_graficos(df)
    
    with tab2:
        mostrar_tabela_dados(df)
    
    with tab3:
        exportar_dados(df)
    
    with tab4:
        configuracoes_sistema()


def mostrar_graficos(df):
    """Mostra gráficos estatísticos"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico: Distribuição por especialidade
        if 'especialidade_recomendada' in df.columns:
            st.subheader("🏥 Especialidades Mais Indicadas")
            
            especialidades = df['especialidade_recomendada'].value_counts().reset_index()
            especialidades.columns = ['Especialidade', 'Quantidade']
            especialidades['Especialidade'] = especialidades['Especialidade'].apply(formatar_nome_especialidade)
            
            fig1 = px.pie(especialidades, 
                         values='Quantidade', 
                         names='Especialidade',
                         title='Distribuição de Encaminhamentos',
                         hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Gráfico: Urgências
        if 'urgencia' in df.columns:
            st.subheader("⚠️ Níveis de Urgência")
            
            urgencias = df['urgencia'].value_counts().reset_index()
            urgencias.columns = ['Urgência', 'Quantidade']
            
            cores = {'alta': '#ff4444', 'média': '#ffaa00', 'baixa': '#44ff44'}
            
            fig2 = px.bar(urgencias, 
                         x='Urgência', 
                         y='Quantidade',
                         title='Distribuição de Urgências',
                         color='Urgência',
                         color_discrete_map=cores)
            st.plotly_chart(fig2, use_container_width=True)
    
    # Gráfico: Atendimentos ao longo do tempo
    if 'timestamp' in df.columns:
        st.subheader("📅 Atendimentos ao Longo do Tempo")
        
        df['data'] = pd.to_datetime(df['timestamp']).dt.date
        atendimentos_dia = df.groupby('data').size().reset_index(name='Quantidade')
        
        fig3 = px.line(atendimentos_dia, 
                      x='data', 
                      y='Quantidade',
                      title='Evolução de Atendimentos',
                      markers=True)
        fig3.update_layout(xaxis_title="Data", yaxis_title="Número de Atendimentos")
        st.plotly_chart(fig3, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Gráfico: Faixa etária
        if 'idade' in df.columns:
            st.subheader("👴 Distribuição por Faixa Etária")
            
            df['faixa_etaria'] = pd.cut(df['idade'], 
                                        bins=[0, 65, 75, 85, 100], 
                                        labels=['60-65', '66-75', '76-85', '86+'])
            
            faixa = df['faixa_etaria'].value_counts().reset_index()
            faixa.columns = ['Faixa Etária', 'Quantidade']
            
            fig4 = px.bar(faixa, 
                         x='Faixa Etária', 
                         y='Quantidade',
                         title='Pacientes por Faixa Etária',
                         color='Quantidade',
                         color_continuous_scale='Blues')
            st.plotly_chart(fig4, use_container_width=True)
    
    with col4:
        # Gráfico: Cidades mais atendidas
        if 'cidade' in df.columns:
            st.subheader("📍 Cidades com Mais Atendimentos")
            
            cidades = df['cidade'].value_counts().head(10).reset_index()
            cidades.columns = ['Cidade', 'Quantidade']
            
            fig5 = px.bar(cidades, 
                         x='Quantidade', 
                         y='Cidade',
                         orientation='h',
                         title='Top 10 Cidades',
                         color='Quantidade',
                         color_continuous_scale='Greens')
            st.plotly_chart(fig5, use_container_width=True)


def mostrar_tabela_dados(df):
    """Mostra tabela com todos os dados"""
    st.subheader("📋 Dados Completos dos Pacientes")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'especialidade_recomendada' in df.columns:
            especialidades = ['Todas'] + list(df['especialidade_recomendada'].unique())
            filtro_esp = st.selectbox("Filtrar por Especialidade:", especialidades)
    
    with col2:
        if 'urgencia' in df.columns:
            urgencias = ['Todas'] + list(df['urgencia'].unique())
            filtro_urg = st.selectbox("Filtrar por Urgência:", urgencias)
    
    with col3:
        if 'cidade' in df.columns:
            cidades = ['Todas'] + list(df['cidade'].unique())
            filtro_cidade = st.selectbox("Filtrar por Cidade:", cidades)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if filtro_esp != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['especialidade_recomendada'] == filtro_esp]
    
    if filtro_urg != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['urgencia'] == filtro_urg]
    
    if filtro_cidade != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['cidade'] == filtro_cidade]
    
    # Mostrar tabela
    st.dataframe(df_filtrado, use_container_width=True)
    
    st.info(f"📊 Mostrando {len(df_filtrado)} de {len(df)} registros")


def exportar_dados(df):
    """Opções de exportação de dados"""
    st.subheader("📥 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Exportar para Excel")
        
        if st.button("⬇️ Preparar Excel", use_container_width=True):
            try:
                # Converter para Excel
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Pacientes')
                
                output.seek(0)
                
                st.download_button(
                    label="💾 Download Excel",
                    data=output,
                    file_name=f"ampi_dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
    
    with col2:
        st.markdown("### 📊 Exportar para CSV")
        
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="⬇️ Baixar CSV",
            data=csv,
            file_name=f"ampi_dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown("---")
    
    st.markdown("### 📊 Integração com Google Sheets")
    st.info("🚧 Funcionalidade em desenvolvimento. Em breve você poderá sincronizar automaticamente com Google Sheets!")
    
    with st.expander("ℹ️ Como configurar Google Sheets"):
        st.write("""
        **Passos para integração futura:**
        
        1. Criar um projeto no Google Cloud Console
        2. Ativar a API do Google Sheets
        3. Criar credenciais de serviço
        4. Baixar o arquivo JSON de credenciais
        5. Configurar no sistema
        
        Documentação: https://developers.google.com/sheets/api
        """)


def configuracoes_sistema():
    """Configurações do sistema"""
    st.subheader("⚙️ Configurações do Sistema")
    
    st.markdown("### 🔐 Segurança")
    
    with st.expander("Alterar Senha do Administrador"):
        nova_senha = st.text_input("Nova senha:", type="password")
        confirmar_senha = st.text_input("Confirmar senha:", type="password")
        
        if st.button("Salvar Senha"):
            if nova_senha == confirmar_senha and len(nova_senha) >= 6:
                st.success("✅ Senha alterada com sucesso!")
                st.info("⚠️ Nota: Por segurança, a senha deve ser alterada diretamente no arquivo config.py")
            else:
                st.error("❌ As senhas não coincidem ou são muito curtas (mínimo 6 caracteres)")
    
    st.markdown("---")
    
    st.markdown("### 🗑️ Gerenciamento de Dados")
    
    with st.expander("⚠️ Zona de Perigo"):
        st.warning("**ATENÇÃO:** As ações abaixo são irreversíveis!")
        
        if st.button("🗑️ Limpar Todos os Dados", type="secondary"):
            st.error("Funcionalidade desabilitada por segurança. Para limpar os dados, delete manualmente o arquivo: dados_pacientes.csv")
    
    st.markdown("---")
    
    st.markdown("### 📊 Informações do Sistema")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.write("**Versão:** 1.0.0")
        st.write("**Modelo LLM:** GPT-3.5-turbo")
        st.write("**Embeddings:** HuggingFace")
    
    with info_col2:
        st.write(f"**Banco de Dados:** {config.DATABASE_FILE}")
        st.write(f"**Total de Perguntas:** {len(PERGUNTAS_AMPI)}")
        st.write(f"**Perguntas por Avaliação:** 10")


# Executar aplicação
if __name__ == "__main__":
    main()