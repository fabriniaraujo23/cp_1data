import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
import io

# Configuração da página
st.set_page_config(
    page_title="CP1 | Fabrini soares ",
    page_icon="📊",
    layout="wide"
)

# --- FUNÇÃO PARA CARREGAR OS DADOS (COM CACHE) ---
@st.cache_data
def load_data():
    try:
        # Carrega o arquivo CSV correto
        df = pd.read_csv('Electric_Vehicle_Population_Data 2.csv')
        return df
    except FileNotFoundError:
        st.error("Erro: O arquivo 'Electric_Vehicle_Population_Data 2.csv' não foi encontrado.")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Carregar os dados
df_original = load_data()

# --- BARRA LATERAL (NAVEGAÇÃO) ---
with st.sidebar:
    # 🔹 Se não tiver imagem, essa linha pode ser comentada
    # st.image("images/perfil.png", width=150)
    st.title("Fabrini soares")
    st.write("Estudante de Engenharia de Software")

    pagina_selecionada = st.radio(
        "Navegue pelas seções:",
        ("Home", "Formação e Experiência", "Skills", "Análise de Dados"),
        key="navigation"
    )

    st.write("---")
    st.write("Projeto de CP1 - FIAP")
    st.write("© 2023 Fabrini soares")

# --- PÁGINAS DO PORTFÓLIO ---
def pagina_home():
    st.title("Fabrini soares")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Informações de Contato")
        st.write("📍 São Paulo, vila matilde")
        st.write("📧 fabriniaraujo23@gmail.com")
        st.write("📞 +55 (11) 945485574")
    with col2:
        st.subheader("Presença Online")
        st.markdown("🔗 [GitHub](https://github.com/fabriniaraujo23)")
    st.markdown("---")
    st.subheader("🎯 Objetivo Profissional")
    st.info("Busco ativamente por uma oportunidade de Jovem Aprendiz, Estágio, Trainee ou Junior na área de Tecnologia da Informação (TI). Meu objetivo é aplicar e aprofundar meus conhecimentos em programação e engenharia de software, contribuindo de forma prática para projetos e desafios do mercado.")

def pagina_formacao_experiencia():
    st.title("📚 Formação Acadêmica e Cursos")
    st.markdown("---")
    st.subheader("🎓 Formação Acadêmica")
    st.markdown("- **Engenharia de Software** - FIAP (Cursando)")
    st.markdown("- **Ensino Médio** (Concluído em Dez/2023)")
    st.markdown("---")
    st.subheader("📜 Cursos de Aprimoramento")
    st.markdown("- **Algoritmos: Aprenda a programar** - FIAP (2024)\n- **Formação Full stack JavaScript** - ALURA (2024)\n- **Introdução a Game Design** - Colégio Internacional Radial (2023)")

def pagina_skills():
    st.title("💡 Habilidades e Competências")
    st.markdown("---")
    st.subheader("🛠️ Tech Skills")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**Linguagens de Programação**")
        st.markdown("- Python\n- Java\n- JavaScript\n- C\n- HTML & CSS")
    with col2:
        st.success("**Frameworks, BDs e Ferramentas**")
        st.markdown("- React.js, Node.js\n- SQL (Oracle, SQLite)\n- Git & GitHub\n- VSCode, IntelliJ\n- Figma")
    with col3:
        st.success("**Conceitos e Outros**")
        st.markdown("- Programação Orientada a Objetos\n- Design Thinking\n- Pacote Office\n- Power BI & Power Query")
    st.markdown("---")
    st.subheader("🌐 Línguas")
    st.markdown("- **Português**: Nativo\n- **Inglês**: Avançado/C1\n- **Espanhol**: Básico")
    st.markdown("---")
    st.subheader("🤝 Soft Skills")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("✓ Responsabilidade\n✓ Inteligência\n✓ Proatividade\n✓ Disciplina")
    with c2:
        st.markdown("✓ Empenho\n✓ Respeito\n✓ Criatividade")

def pagina_analise_dados():
    st.title("📊 Análise de Dados: Veículos Elétricos")
    st.markdown("---")

    if df_original.empty:
        return

    st.subheader("1. Estrutura dos Dados")
    st.dataframe(df_original.head())
    st.write("Dimensões:", df_original.shape)

    st.write("---")
    st.subheader("2. Distribuição por Fabricante (Top 10)")
    top_fabricantes = df_original['Make'].value_counts().head(10)
    st.bar_chart(top_fabricantes)

    st.write("---")
    st.subheader("3. Evolução de Veículos por Ano de Modelo")
    if 'Model Year' in df_original.columns:
        veiculos_ano = df_original.groupby("Model Year").size().reset_index(name="Quantidade")
        fig_line = px.line(veiculos_ano, x="Model Year", y="Quantidade", markers=True,
                           title="Evolução de Veículos Elétricos por Ano de Modelo")
        st.plotly_chart(fig_line)

    st.write("---")
    st.subheader("4. Tipos de Veículos Elétricos")
    if 'Electric Vehicle Type' in df_original.columns:
        tipos = df_original['Electric Vehicle Type'].value_counts()
        fig_pie = px.pie(values=tipos.values, names=tipos.index, title="Distribuição dos Tipos de Veículos Elétricos")
        st.plotly_chart(fig_pie)

    st.write("---")
    st.subheader("5. Distribuição Geográfica por Estado")
    if 'State' in df_original.columns:
        estados = df_original['State'].value_counts().reset_index()
        estados.columns = ['Estado', 'Quantidade']
        fig_map = px.choropleth(estados,
                                locations='Estado',
                                locationmode="USA-states",
                                color='Quantidade',
                                scope="usa",
                                title="Distribuição de Veículos Elétricos por Estado")
        st.plotly_chart(fig_map)

# --- LÓGICA DE EXIBIÇÃO DE PÁGINAS ---
if pagina_selecionada == "Home":
    pagina_home()
elif pagina_selecionada == "Formação e Experiência":
    pagina_formacao_experiencia()
elif pagina_selecionada == "Skills":
    pagina_skills()
elif pagina_selecionada == "Análise de Dados":
    pagina_analise_dados()
