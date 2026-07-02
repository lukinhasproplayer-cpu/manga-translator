import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from deep_translator import GoogleTranslator
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Manga HUD Lens", layout="wide")

st.title("📖 MANGA HUD LENS")
st.write("Envie uma imagem, selecione a área e traduza o texto automaticamente")

# OCR (japonês + inglês)
reader = easyocr.Reader(['ja', 'en'], gpu=False)

# Upload da imagem
uploaded_file = st.file_uploader("📤 Envie uma imagem de mangá", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    st.subheader("🧠 Selecione a área do texto (HUD)")

    # Canvas para desenhar área
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

        if canvas_result.json_data is None:
            st.warning("Selecione uma área primeiro!")
        else:
            objects = canvas_result.json_data["objects"]

            if len(objects) == 0:
                st.warning("Você precisa marcar uma área!")
            else:
                obj = objects[0]

                left = int(obj["left"])
                top = int(obj["top"])
                width = int(obj["width"])
                height = int(obj["height"])

                # recorta imagem
                cropped = img_array[top:top+height, left:left+width]

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
                        source='auto',
                        target='pt'
                    ).translate(text)

                    st.subheader("🌍 Tradução")
                    st.success(translated)
                else:
                    st.error("Não foi possível ler texto na área selecionada")
