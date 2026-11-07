import sys
from pathlib import Path

# Ensure the project root is available for package imports.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.agent import run_agent


st.set_page_config(
    page_title="VentureScope",
    page_icon="🔭",
    layout="wide"
)

# Dashboard styling
st.markdown("""
<style>
    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
    }

    [data-testid="stChatMessage"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.title("🔭 VentureScope")
    st.caption("AI Research & Intelligence")

    st.divider()

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("WORKSPACE")
    st.write("💬 Conversations")
    st.write("📄 Research reports")
    st.write("🌍 Published intelligence")

    st.divider()
    st.caption("Built with 💙 by Dayve")


# Main dashboard
st.title("VentureScope")
st.subheader("Your AI research and intelligence workspace.")

st.write(
    "Ask questions, investigate ideas, and generate "
    "research that you can share with others."
)

st.divider()


# Welcome message
if not st.session_state.messages:
    st.markdown("### What would you like to investigate?")
    st.write(
        "Ask VentureScope a question or give it a research task."
    )


# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat interface
prompt = st.chat_input("Ask VentureScope anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("VentureScope is thinking..."):
            try:
                response = run_agent(prompt)
                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as error:
                st.error(f"Request failed: {error}")