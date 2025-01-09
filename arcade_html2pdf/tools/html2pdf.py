from arcade.sdk import tool
from typing import Annotated

from arcade_html2pdf.tools.adapter import HTML2PDFAdapter, PDFFormat

@tool
def convert_html_to_pdf(
    html_url: Annotated[str, "URL of the HTML to convert to PDF"],
    format: Annotated[PDFFormat, "PDF format"] = PDFFormat.A4,
    file_name: Annotated[str, "Name of the PDF file without extension"] = "output"
) -> str:
    """Convert HTML to PDF and save it to the Downloads folder"""

    try:
        adapter = HTML2PDFAdapter()
        response: str = adapter.generate_pdf(html_url, format, file_name)
        print(response)
        return response
    except Exception as e:
        return f"Error: {str(e)}"
