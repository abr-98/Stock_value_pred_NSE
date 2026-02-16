import requests
from pathlib import Path

def download_pdf(
    url: str,
    save_path: str,
    timeout: int = 30,
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
) -> str:
    """
    Downloads a PDF from a URL and saves it locally.

    Returns:
        Path to saved PDF
    """
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/pdf",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=timeout
    )
    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)

    return str(save_path)
