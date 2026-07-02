import cv2

from capture.screen_capture import ScreenCapture
from ocr.ocr_engine import OCREngine

print("Iniciando captura...")
cap = ScreenCapture()

ocr = OCREngine()

while True:

    frame = cap.get_frame()

    if frame is None:
        continue

    textos = ocr.read(frame)

    for t in textos:

        print(t["texto"])

        pts = t["box"]

        x = int(pts[0][0])
        y = int(pts[0][1])

        cv2.putText(
            frame,
            t["texto"],
            (x, y-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            1
        )

    cv2.imshow("OCR", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()