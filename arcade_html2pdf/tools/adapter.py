import httpx
import os
from enum import Enum
from pathlib import Path
from typing import Annotated
from dotenv import load_dotenv

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
    api_key: Annotated[str, "HTML2PDF API key"]
    base_url: Annotated[str, "HTML2PDF Base Url"] = "https://api.html2pdf.app/v1/generate"

    def __init__(self, arcade_env: str = "~/.arcade/arcade.env"):
        load_dotenv(arcade_env)
        self.api_key = os.getenv("HTML2PDF_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided")

    def get_download_folder(self) -> Path:
        return Path(os.path.expanduser('~/.arcade/'))

    def generate_pdf(
        self,
        html_url: Annotated[str, "URL of the HTML to convert to PDF"],
        format: Annotated[PDFFormat, "PDF format"] = PDFFormat.A4,
        file_name: Annotated[str, "Name of the PDF file"] = "output"
    ) -> str:
        if not html_url:
            return "Error: HTML URL must be provided"

        params = {
            'html': html_url,
            'apiKey': self.api_key,
            'format': format.value
        }
        response = httpx.get(self.base_url, params=params)
        if response.status_code == 200:
            download_folder = self.get_download_folder()
            download_folder.mkdir(parents=True, exist_ok=True)
            pdf_path = download_folder / f"{file_name}.pdf"
            pdf_path.write_bytes(response.content)
            if pdf_path.exists():
                return f"PDF successfully generated at {pdf_path}"
            else:
                return "Error: PDF file could not be created"
        else:
            return f"Error: Failed to generate PDF, status code {response.status_code}"
