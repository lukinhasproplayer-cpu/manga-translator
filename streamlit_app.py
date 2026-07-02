import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Manga Lens - CAPTURE 3", layout="centered")

st.title("📖 Manga Lens - CAPTURE 3")
st.write("App de captura funcionando 🚀")

# Estado do app
if "captured" not in st.session_state:
    st.session_state.captured = False

if "time" not in st.session_state:
    st.session_state.time = None


# BOTÃO PRINCIPAL
if st.button("📸 Capturar tela"):
    st.session_state.captured = True
    st.session_state.time = datetime.now().strftime("%H:%M:%S")
    st.success("📸 Captura realizada com sucesso!")


# MOSTRA RESULTADO
if st.session_state.captured:
    st.info(f"Última captura: {st.session_state.time}")

    st.image(
        "https://i.imgur.com/4AiXzf8.jpg",
        caption="Simulação de captura de tela"
    )

    if st.button("🔄 Nova captura"):
        st.session_state.captured = False
        st.rerun()
