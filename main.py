import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pexels.downloader import fetch_pexels_image
from quote_generator.image_creator import create_image_with_quote

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_quote():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Kamu adalah pembuat kutipan motivasi."},
            {"role": "user", "content": "Buatkan 1 kutipan motivasi pendek (maksimum 15 kata) dalam bahasa Indonesia. Tanpa nama penulis."}
        ],
        temperature=0.8,
        max_tokens=60
    )
    return response.choices[0].message.content.strip()

def main():
    try:
        n = int(input("📌 Berapa banyak quote image yang ingin kamu buat? "))
    except ValueError:
        print("⚠️ Masukkan angka yang valid.")
        return

    for i in range(n):
        bg_path = fetch_pexels_image(query="gradient abstract")
        if not bg_path:
            print("❌ Gagal mengambil gambar background.")
            continue

        quote = generate_quote()
        output_path = OUTPUT_DIR / f"quote_{i+1:03}.png"
        create_image_with_quote(quote, bg_path, output_path)
        print(f"✅ Quote #{i+1} berhasil dibuat → {output_path}")

if __name__ == "__main__":
    main()
