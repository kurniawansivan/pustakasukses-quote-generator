import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
FONT_PATH = "/Library/Fonts/Supplemental/Arial Bold.ttf"
IMAGE_SIZE = (1080, 1920)
FONT_SIZE = 60
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (30, 30, 30)

def generate_quote():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a quote generator."},
            {"role": "user", "content": "Give me a short motivational quote under 15 words. No author attribution."}
        ],
        temperature=0.8,
        max_tokens=60
    )
    return response.choices[0].message.content.strip()

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

def create_image(quote, index):
    img = Image.new("RGB", IMAGE_SIZE, color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    lines = wrap_text(draw, quote, font, max_width=IMAGE_SIZE[0] * 0.85)
    total_height = len(lines) * FONT_SIZE + (len(lines) - 1) * 20
    y = (IMAGE_SIZE[1] - total_height) // 2
    
    for line in lines:
        w = draw.textlength(line, font=font)
        x = (IMAGE_SIZE[0] - w) // 2
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)
        y += FONT_SIZE + 20

    output_path = OUTPUT_DIR / f"quote_{index:03}.png"
    img.save(output_path)
    print(f"✅ Saved: {output_path}")

def main(n=90):
    for i in range(n):
        quote = generate_quote()
        create_image(quote, i+1)

if __name__ == "__main__":
    main(n=3)  # Change to 90 later
