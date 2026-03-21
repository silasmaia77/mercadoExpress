import streamlit as st
import pandas as pd
import sqlite3
from src.agent import get_agent
from src.gerar_relatorio import gerar_relatorio_txt

# Configuração da Página
st.set_page_config(page_title="MercadoExpress Chat", layout="wide")

# --- CSS para deixar estilo "Clean GPT" ---
st.markdown("""
<style>
    .stChatMessage { padding: 1rem; border-radius: 10px; margin-bottom: 10px; }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #f0f2f6; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #ffffff; border: 1px solid #e0e0e0; }
    h1 { color: #333; font-size: 1.8rem; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (ADMIN) ---
with st.sidebar:
    st.header("🛠️ Painel Administrativo")

    # Seção de Pedidos
    with st.expander("📦 Últimos Pedidos (SQLite)", expanded=False):
        if st.button("Atualizar Tabela"):
            try:
                conn = sqlite3.connect("data/mercado.db")
                df = pd.read_sql_query("SELECT id, cliente_nome, total, metodo_pagamento FROM pedidos ORDER BY id DESC LIMIT 10", conn)
                conn.close()
                st.dataframe(df, hide_index=True)
            except:
                st.warning("Sem dados ainda.")

    # Seção de Relatórios
    with st.expander("📄 Relatórios", expanded=False):
        if st.button("Gerar Relatório Quinzenal"):
            msg = gerar_relatorio_txt()
            st.success(msg)

    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.session_state.agent_memory = None
        st.rerun()

# --- LÓGICA DO CHAT (PRINCIPAL) ---

st.title("🛒 MercadoExpress AI")
st.caption("Atendente Virtual Inteligente")

# 1. Inicializar Histórico no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Carregar Agente (Cacheado para não perder memória)
@st.cache_resource
def load_cached_agent():
    return get_agent()

agent = load_cached_agent()

# 3. Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input do Usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = agent.chat(prompt)
                response_text = str(response)
                st.markdown(response_text)

                # Salva resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Erro no agente: {e}")
