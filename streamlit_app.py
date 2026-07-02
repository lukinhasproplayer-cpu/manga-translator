import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Manga HUD Lens", layout="wide")

st.title("📖 MANGA HUD LENS v2")
st.write("Envie uma imagem de mangá e marque o texto para traduzir")

# Upload da imagem
uploaded_file = st.file_uploader("📤 Envie uma imagem de mangá", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("🧠 Marque a área do texto")

    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.2)",
        stroke_width=2,
        stroke_color="#00FF00",
        background_image=image,   # 👈 AQUI é o fix principal
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="rect",
        key="canvas"
    )

    # Mostrar resultado bruto do canvas
    if canvas_result.json_data is not None:
        st.write("📦 Dados da seleção:")
        st.json(canvas_result.json_data)
