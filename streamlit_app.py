import streamlit as st
from PIL import Image
import numpy as np

st.title("📖 Manga Lens - CAPTURE 2")

st.write("📸 Tire uma foto do mangá abaixo")

# 📷 câmera
img_file = st.camera_input("Capturar imagem")

if img_file:
    image = Image.open(img_file)
    img_array = np.array(image)

    st.success("Imagem capturada com sucesso!")

    # mostrar imagem original
    st.image(image, caption="Imagem capturada", use_container_width=True)

    # debug: mostrar tamanho
    st.write("Tamanho da imagem:", img_array.shape)
else:
    st.info("Aguardando captura...")
