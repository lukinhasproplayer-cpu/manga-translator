import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.title("📖 Manga Lens - CAPTURE 3 (OCR)")

st.write("📸 Tire uma foto do mangá e vamos detectar o texto")

# 📷 câmera
img_file = st.camera_input("Capturar imagem")

# 🔥 carregar OCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en', 'ja'], gpu=False)

ocr = load_ocr()

if img_file:
    image = Image.open(img_file)
    img_array = np.array(image)

    st.image(image, caption="Imagem capturada", use_container_width=True)

    st.info("🔍 Detectando texto...")

    # OCR
    results = ocr.readtext(img_array)

    if results:
        st.success(f"{len(results)} textos encontrados!")

        for bbox, text, prob in results:
            if text.strip():
                st.write(f"📝 **{text}** (confiança: {prob:.2f})")

    else:
        st.warning("Nenhum texto detectado")
else:
    st.info("Aguardando captura...")
