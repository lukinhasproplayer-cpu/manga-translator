
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from googletrans import Translator
import textwrap
import tempfile
import os

st.set_page_config(page_title="Manga Lens PRO FINAL", layout="wide")
st.title("📖 Manga Lens PRO FINAL (produto completo)")

@st.cache_resource
def load_models():
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    translator = Translator()
    return ocr, translator

ocr, translator = load_models()

img_file = st.camera_input("📸 Tire uma foto do mangá")


# 🔥 agrupa falas por proximidade
def group_boxes(data, threshold=90):
    groups = []

    for bbox, text in data:
        x = int(bbox[0][0])
        y = int(bbox[0][1])

        found = False

        for g in groups:
            gx, gy = g["center"]

            if abs(x - gx) < threshold and abs(y - gy) < threshold:
                g["items"].append((bbox, text))
                g["center"] = ((gx + x) // 2, (gy + y) // 2)
                found = True
                break

        if not found:
            groups.append({
                "items": [(bbox, text)],
                "center": (x, y)
            })

    return groups


def create_mask(img, data):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    for bbox, _ in data:
        pts = np.array(bbox, dtype=np.int32)
        cv2.fillPoly(mask, [pts], 255)

    return mask


def draw_manga_text(img, text, center):
    wrapped = textwrap.fill(text, width=28)
    lines = wrapped.split("\n")

    x, y = center

    for i, line in enumerate(lines):
        cv2.putText(
            img,
            line,
            (int(x), int(y + i * 24)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255),
            2,
            cv2.LINE_AA
        )


if img_file:
    image = Image.open(img_file)
    img = np.array(image)

    st.image(image, caption="Original", use_container_width=True)

    st.info("🔍 Processando mangá...")

    result = ocr.ocr(img, cls=True)

    if result and result[0]:
        img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        data = []

        # 1. OCR
        for line in result[0]:
            bbox = line[0]
            text = line[1][0]

            if text.strip():
                data.append((bbox, text))

        # 2. agrupar por balão
        groups = group_boxes(data)

        # 3. remover texto original (inpainting)
        mask = create_mask(img_cv, data)
        img_clean = cv2.inpaint(img_cv, mask, 3, cv2.INPAINT_TELEA)

        # 4. traduzir por grupo (contexto)
        for g in groups:
            full_text = " ".join([t[1] for t in g["items"]])

            translated = translator.translate(full_text, dest='pt').text

            draw_manga_text(img_clean, translated, g["center"])

        # 5. converter para download
        final_img = cv2.cvtColor(img_clean, cv2.COLOR_BGR2RGB)

        st.success("🔥 Manga traduzido com sucesso!")

        st.image(final_img, caption="Resultado FINAL", use_container_width=True)

        # 🔥 botão de download
        _, buffer = cv2.imencode(".png", img_clean)

        st.download_button(
            label="📥 Baixar imagem traduzida",
            data=buffer.tobytes(),
            file_name="manga_traduzido.png",
            mime="image/png"
        )

    else:
        st.warning("Nenhum texto detectado")
