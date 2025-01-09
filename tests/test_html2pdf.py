import pytest
from unittest.mock import patch

from arcade_html2pdf.tools.html2pdf import convert_html_to_pdf

@pytest.fixture
def mock_html2pdf_adapter():
    with patch('arcade_html2pdf.tools.adapter.HTML2PDFAdapter') as mock:
        yield mock.return_value


@pytest.fixture
def mock_httpx_get():
    with patch('httpx.get') as mock:
        yield mock


@pytest.fixture
def mock_load_dotenv():
    with patch('arcade_html2pdf.tools.adapter.load_dotenv') as mock:
        yield mock


@pytest.fixture
def mock_getenv():
    with patch('os.getenv') as mock:
        mock.return_value = "test_api_key"
        yield mock


@pytest.fixture
def mock_path_write_bytes():
    with patch('pathlib.Path.write_bytes') as mock:
        yield mock


@pytest.fixture
def mock_path_exists():
    with patch('pathlib.Path.exists') as mock:
        mock.return_value = True
        yield mock


@pytest.mark.usefixtures("mock_html2pdf_adapter", "mock_httpx_get", "mock_load_dotenv", "mock_getenv", "mock_path_write_bytes", "mock_path_exists")
def test_successful_convert_html_to_pdf(mock_html2pdf_adapter, mock_httpx_get):
    mock_response = mock_httpx_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'%PDF-1.4\n%...'

    test_url: str = "https://docs.arcade-ai.com/home/install/local"
    
    response = convert_html_to_pdf(test_url)
    assert "PDF successfully generated at" in response

@pytest.mark.usefixtures("mock_html2pdf_adapter", "mock_httpx_get", "mock_load_dotenv", "mock_getenv", "mock_path_write_bytes", "mock_path_exists")
def test_failed_convert_html_to_pdf_due_to_status_code(mock_html2pdf_adapter, mock_httpx_get):
    mock_response = mock_httpx_get.return_value
    mock_response.status_code = 500
    mock_response.content = b'Internal Server Error'

    test_url: str = "https://docs.arcade-ai.com/home/install/local"
    
    response = convert_html_to_pdf(test_url)
    assert "Error: Failed to generate PDF, status code 500" in response
