from arcade.sdk import tool, ToolContext
from typing import Annotated

from arcade_html2pdf.tools.adapter import HTML2PDFAdapter, PDFFormat

@tool
def convert_html_to_pdf(
    context: ToolContext,
    html_url: Annotated[str, "URL of the HTML to convert to PDF"],
    format: Annotated[PDFFormat, "PDF format"] = PDFFormat.A4
) -> str:
    """Convert HTML to PDF and save it to the Downloads folder"""

    adapter = HTML2PDFAdapter(api_key=context.authorization.token)
    pdf_content = adapter.generate_pdf(html_url, format)
    if pdf_content:
        return "PDF generated and saved successfully."
    else:
        return "Failed to generate PDF."
