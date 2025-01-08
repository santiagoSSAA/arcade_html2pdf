from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (
    EvalRubric,
    EvalSuite,
    SimilarityCritic,
    tool_eval,
)

import arcade_html2pdf
from arcade_html2pdf.tools.html2pdf import convert_html_to_pdf

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("HTML2PDF_API_KEY")

# Evaluation rubric
rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
)


catalog = ToolCatalog()
catalog.add_module(arcade_html2pdf)


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

    suite.add_case(
        name="Downloading Google as PDF",
        user_message=(
            "I want to download https://www.google.com/ as a PDF file. "
        ),
        expected_tool_calls=[(convert_html_to_pdf, {"api_key": API_KEY})],
        rubric=rubric,
        critics=[
            SimilarityCritic(critic_field="api_key", weight=0.9),
        ]
    )

    return suite
