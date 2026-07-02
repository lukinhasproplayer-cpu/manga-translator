import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from googletrans import Translator
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Manga HUD Lens", layout="wide")

st.title("📖 MANGA HUD LENS - OCR + TRADUÇÃO")
st.write("Envie a imagem, selecione a área e traduza automaticamente")

# Inicializa OCR e tradutor
reader = easyocr.Reader(['ja', 'en'], gpu=False)
translator = Translator()

# Upload da imagem
uploaded_file = st.file_uploader("📤 Envie uma imagem de mangá", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.subheader("🧠 Marque a área do texto (HUD)")

    # CANVAS para seleção (HUD)
    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.2)",
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=600,
        width=800,
        drawing_mode="rect",
        key="canvas",
    )

    if st.button("📖 Ler e Traduzir"):
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]

            if len(objects) == 0:
                st.warning("Selecione uma área primeiro!")
            else:
                # pega primeira área desenhada
                obj = objects[0]

                left = int(obj["left"])
                top = int(obj["top"])
                width = int(obj["width"])
                height = int(obj["height"])

                # recorta imagem
                cropped = img_array[top:top+height, left:left+width]

                st.image(cropped, caption="Área selecionada", use_container_width=True)

                # OCR
                result = reader.readtext(cropped, detail=0)
                text = " ".join(result)

                st.subheader("📝 Texto detectado:")
                st.write(text)

                # tradução
                if text.strip():
                    translated = translator.translate(text, dest="pt")
                    st.subheader("🌍 Tradução:")
                    st.success(translated.text)
                else:
                    st.error("Nenhum texto encontrado")
