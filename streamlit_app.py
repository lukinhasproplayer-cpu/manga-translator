import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from deep_translator import GoogleTranslator
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Manga HUD Lens", layout="wide")

st.title("📖 MANGA HUD LENS v2")
st.write("Envie a imagem, selecione o texto e traduza automaticamente")

# OCR inicializa uma vez
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['ja', 'en'], gpu=False)

reader = load_ocr()

uploaded_file = st.file_uploader("📤 Envie uma imagem de mangá", type=["png", "jpg", "jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    st.subheader("🧠 Marque a área do texto")

    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.2)",
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=600,
        width=800,
        drawing_mode="rect",
        key="canvas"
    )

    if st.button("📖 Ler e Traduzir"):

        if not canvas_result.json_data:
            st.warning("Desenhe uma área primeiro!")
            st.stop()

        objects = canvas_result.json_data.get("objects", [])

        if len(objects) == 0:
            st.warning("Nenhuma área selecionada!")
            st.stop()

        obj = objects[0]

        left = int(obj["left"])
        top = int(obj["top"])
        width = int(obj["width"])
        height = int(obj["height"])

        # proteção contra erro de corte
        h, w, _ = img_array.shape
        left = max(0, left)
        top = max(0, top)
        right = min(w, left + width)
        bottom = min(h, top + height)

        cropped = img_array[top:bottom, left:right]

        st.subheader("🖼️ Área selecionada")
        st.image(cropped, use_container_width=True)

        # OCR
        result = reader.readtext(cropped, detail=0)
        text = " ".join(result)

        st.subheader("📝 Texto detectado")
        st.write(text if text else "Nenhum texto encontrado")

        # tradução
        if text.strip():
            translated = GoogleTranslator(
                source="auto",
                target="pt"
            ).translate(text)

            st.subheader("🌍 Tradução")
            st.success(translated)

        else:
            st.error("Não foi possível ler texto na área selecionada")
