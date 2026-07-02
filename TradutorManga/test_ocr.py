import cv2

from capture.screen_capture import ScreenCapture
from ocr.ocr_engine import OCREngine

print("Iniciando captura...")
cap = ScreenCapture()

print("Carregando OCR...")
ocr = OCREngine()

while True:
    frame = cap.get_frame()

    if frame is None:
        continue

    try:
        textos = ocr.read(frame)
        print(textos)
    except Exception as e:
        print(e)

    cv2.imshow("Tela", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()