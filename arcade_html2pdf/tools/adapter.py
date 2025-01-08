import httpx
import os
from enum import Enum
from pathlib import Path
from typing import Annotated

class PDFFormat(Enum):
    LETTER = "Letter"
    LEGAL = "Legal"
    TABLOID = "Tabloid"
    LEDGER = "Ledger"
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"

class HTML2PDFAdapter:
    def __init__(self, api_key: Annotated[str, "API key for HTML2PDF service"] = None):
        if not api_key:
            raise ValueError("API key must be provided")
        self.api_key = api_key
        self.base_url = "https://api.html2pdf.app/v1/generate"

    def get_download_folder(self) -> Path:
        if os.name == 'nt':  # Windows
            return Path(os.path.join(os.environ['USERPROFILE'], 'Downloads'))
        elif os.name == 'posix':
            if 'linux' in os.uname().sysname.lower():  # Linux
                return Path(os.path.join(os.path.expanduser('~'), 'Downloads'))
            elif 'darwin' in os.uname().sysname.lower():  # macOS
                return Path(os.path.join(os.path.expanduser('~'), 'Downloads'))
        raise EnvironmentError("Unsupported OS")

    def generate_pdf(self, html_url: Annotated[str, "URL of the HTML to convert to PDF"], format: Annotated[PDFFormat, "PDF format"] = PDFFormat.A4) -> bool:
        if not html_url:
            raise ValueError("HTML URL must be provided")

        params = {
            'html': html_url,
            'apiKey': self.api_key,
            'format': format.value
        }
        response = httpx.get(self.base_url, params=params)
        if response.status_code == 200:
            download_folder = self.get_download_folder()
            pdf_path = download_folder / "output.pdf"
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            return True
        response.raise_for_status()
        return False
