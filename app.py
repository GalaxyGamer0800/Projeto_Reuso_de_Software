"""
Módulo: app
Descrição: Interface Web Interativa em Streamlit para o RentalFramework.
Técnica: Web UI / Streamlit Chat / Agentic Integration (Tool Calling)
"""

import os
import streamlit as st
from rental_agent import RentalAgentEngine

# Configuração da página
st.set_page_config(
    page_title="RentalFramework - Assistente IA",
    page_icon="🏠",
    layout="wide"
)

# Cabeçalho principal
st.title("🏠 RentalFramework — Atendimento Inteligente")
st.caption("Ecossistema de Locação de Imóveis | Microsserviços, Template Method e Agente IA (Gemini)")

# Barra lateral: Configurações, Arquitetura e Atalhos de Demonstração
with st.sidebar:
    st.header("🔑 Configuração do Agente")
    api_key_input = st.text_input(
        "Chave da API Gemini:",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="Cole sua chave do AI Studio aqui..."
    )

    if st.button("Conectar / Reiniciar Agente", use_container_width=True):
        if api_key_input:
            try:
                st.session_state.agent_engine = RentalAgentEngine(api_key=api_key_input)
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Agente Gemini conectado! Como posso ajudar com suas reservas hoje?"
                    }
                ]
                st.success("Agente conectado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao conectar: {e}")
        else:
            st.warning("Informe uma API Key válida antes de conectar.")

    st.divider()
    st.header("⚙️ Arquitetura Ativa")
    st.markdown("""
    - 🟢 **API Gateway:** Porta `8000`
    - 🏢 **Property Service:** Porta `8001`
    - 📅 **Booking Service:** Porta `8002`
    - 💳 **Payment Service:** Porta `8003`
    """)

    st.divider()
    st.header("🧩 Hotspots do Framework")
    st.info("🏙️ **UrbanRent:** Aptos urbanos (Mín. 1 diária | Desc. ≥ 7 dias)")
    st.info("🏖️ **BeachHouseRent:** Casas de praia (Mín. 3 diárias | Desc. ≥ 14 dias)")

# Inicialização automática caso a variável de ambiente já exista
if "agent_engine" not in st.session_state:
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        try:
            st.session_state.agent_engine = RentalAgentEngine(api_key=env_key)
        except Exception:
            st.session_state.agent_engine = None
    else:
        st.session_state.agent_engine = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Olá! Sou o assistente virtual do **RentalFramework**.\n\n"
                "Cole sua **Chave da API Gemini** na barra lateral à esquerda e clique em **Conectar** para começarmos. "
                "Depois disso, você pode me pedir coisas como:\n"
                "- *'Quais imóveis estão disponíveis em Recife?'*\n"
                "- *'Quero reservar o apartamento APT-URB-202 por 7 dias'*\n"
                "- *'Realizar pagamento da reserva 1 via PIX'*"
            )
        }
    ]

# Renderização do histórico da conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de mensagens do usuário
if prompt := st.chat_input("Digite sua solicitação em linguagem natural..."):
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa a resposta com o Agente
    with st.chat_message("assistant"):
        if st.session_state.get("agent_engine") is None:
            aviso = "⚠️ O agente ainda não foi inicializado. Cole sua API Key na barra lateral e clique em **Conectar / Reiniciar Agente**."
            st.warning(aviso)
            st.session_state.messages.append({"role": "assistant", "content": aviso})
        else:
            with st.spinner("O Agente Gemini está consultando os microsserviços via API Gateway..."):
                resposta = st.session_state.agent_engine.processar_mensagem(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})