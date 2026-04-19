import requests
from pathlib import Path


def download_pdf(url, save_dir="pdfs", filename=None):
    # create folder if not exists
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    # auto filename from URL if not provided
    if not filename:
        filename = url.split("/")[-1].split("?")[0]

        if not filename.endswith(".pdf"):
            filename += ".pdf"

    file_path = Path(save_dir) / filename

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            print(f"Failed to download: {url}")
            return None

        with open(file_path, "wb") as f:
            f.write(res.content)

        print(f"Saved: {file_path}")
        return str(file_path)

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None