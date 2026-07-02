from PIL import Image, ImageDraw, ImageFont
import textwrap


def get_font_size(draw, text, max_width, max_height, font_path=None):
    # começa grande e vai reduzindo até caber
    font_size = 40

    while font_size > 10:
        font = ImageFont.truetype(font_path or "arial.ttf", font_size)

        lines = textwrap.wrap(text, width=15)
        line_height = font_size + 5

        total_height = line_height * len(lines)
        max_line_width = max([draw.textlength(line, font=font) for line in lines]) if lines else 0

        if max_line_width <= max_width and total_height <= max_height:
            return font, lines

        font_size -= 2

    font = ImageFont.load_default()
    return font, textwrap.wrap(text, width=15)


def render_text(image, translations):
    img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for box, text in translations:

        # calcula retângulo do balão (bbox)
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]

        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)

        max_width = x2 - x1
        max_height = y2 - y1

        font, lines = get_font_size(draw, text, max_width, max_height)

        total_text_height = len(lines) * (font.size + 5)
        y_offset = y1 + (max_height - total_text_height) // 2

        for line in lines:
            text_width = draw.textlength(line, font=font)
            x_offset = x1 + (max_width - text_width) // 2

            draw.text((x_offset, y_offset), line, fill=(0, 0, 0), font=font)

            y_offset += font.size + 5

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)