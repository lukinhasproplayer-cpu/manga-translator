import easyocr

class OCREngine:
    def __init__(self):
        print("Carregando EasyOCR...")

        self.reader = easyocr.Reader(
            ['ja', 'en'],
            gpu=False
        )

    def read(self, image):
        resultado = self.reader.readtext(image)

        textos = []

        for box, texto, conf in resultado:
            if conf > 0.30:
                textos.append({
                    "texto": texto,
                    "box": box,
                    "conf": conf
                })

        return textos