import streamlit as st
import cv2
import numpy as np
from core import run_ocr, create_mask, inpaint, translate
from render import render

st.set_page_config(
    page_title="Manga Translator AI",
    layout="wide"
)

st.title("📖 Manga Translator AI")
st.caption("Tradução automática de mangás com IA")