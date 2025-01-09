from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (
    EvalRubric,
    EvalSuite,
    SimilarityCritic,
    tool_eval,
)

from arcade_html2pdf.tools.adapter import PDFFormat
from arcade_html2pdf.tools.html2pdf import convert_html_to_pdf

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
    fail_on_tool_selection=True,
    tool_selection_weight=1.0,
)


catalog = ToolCatalog()
catalog.add_tool(convert_html_to_pdf, "html2pdf")


@tool_eval()
def html2pdf_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="html2pdf Tools Evaluation",
        system_message=(
            "You are an AI assistant with access to html2pdf tools. "
            "The tools are designed to help users convert HTML pages to PDF files. "
            "You are expected to use the tools to assist users in generating PDF files. "
        ),
        catalog=catalog,
        rubric=rubric,
    )

    html_url = "https://docs.arcade-ai.com/home/install/local"
    suite.add_case(
        name="Downloading Arcade AI docs as PDF in A4 format",
        user_message=(
            f"I want to download {html_url} as a PDF file in A4 format. "
        ),
        expected_tool_calls=[(convert_html_to_pdf, {
            "html_url": html_url,
            "format": PDFFormat.A4.value,
        })],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="html_url", weight=0.5),
            SimilarityCritic(critic_field="format", weight=0.5),
        ]
    )

    return suite
