import cv2
import numpy as np
import easyocr
from googletrans import Translator

reader = easyocr.Reader(['en', 'ja', 'ko'])
translator = Translator()


def run_ocr(image):
    return reader.readtext(image)


def create_mask(image, ocr_result):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    for box, text, conf in ocr_result:
        pts = np.array(box).astype(np.int32)
        cv2.fillPoly(mask, [pts], 255)

    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask


def inpaint(image, mask):
    return cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)


def translate(ocr_result):
    output = []

    for box, text, conf in ocr_result:
        if text.strip():
            try:
                t = translator.translate(text, dest="pt").text
            except:
                t = text
            output.append((box, t))

    return output