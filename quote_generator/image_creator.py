from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

FONT_PATH = "/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SIZE = 60
TEXT_COLOR = (255, 255, 255)
IMAGE_SIZE = (1080, 1920)

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def create_image_with_quote(quote, bg_image_path: Path, output_path: Path):
    bg = Image.open(bg_image_path).convert("RGB").resize(IMAGE_SIZE)

    # Add black semi-transparent overlay
    overlay = Image.new("RGB", IMAGE_SIZE, (0, 0, 0))
    blended = Image.blend(bg, overlay, alpha=0.4)

    draw = ImageDraw.Draw(blended)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    lines = wrap_text(draw, quote, font, max_width=IMAGE_SIZE[0] * 0.85)
    total_height = len(lines) * FONT_SIZE + (len(lines) - 1) * 20
    y = (IMAGE_SIZE[1] - total_height) // 2

    for line in lines:
        w = draw.textlength(line, font=font)
        x = (IMAGE_SIZE[0] - w) // 2
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += FONT_SIZE + 20

    blended.save(output_path)
