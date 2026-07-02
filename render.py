import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap


def render(image, translations):
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()

    for box, text in translations:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]

        x1, y1 = min(xs), min(ys)

        wrapped = textwrap.wrap(text, width=15)

        y = y1

        for line in wrapped:
            draw.text((x1, y), line, fill=(0,0,0), font=font)
            y += 15

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)