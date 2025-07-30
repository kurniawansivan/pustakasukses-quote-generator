import os
import random
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PEXELS_API_KEY")
HEADERS = {"Authorization": API_KEY}
DOWNLOAD_DIR = Path("backgrounds")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def fetch_pexels_image(query="gradient abstract", orientation="portrait", total_pool=30):
    url = "https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": total_pool,
        "page": 1
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print("❌ Failed to fetch from Pexels:", response.status_code)
        return None

    photos = response.json().get("photos", [])
    if not photos:
        print("❌ No photos found.")
        return None

    selected = random.choice(photos)
    photo_url = selected["src"]["large2x"]

    file_path = DOWNLOAD_DIR / f"pexels_bg_{selected['id']}.jpg"
    if not file_path.exists():
        img_data = requests.get(photo_url).content
        with open(file_path, "wb") as f:
            f.write(img_data)

    return file_path
