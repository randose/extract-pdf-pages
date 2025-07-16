from pathlib import Path
from pypdf import PdfReader
import pytest
import os
from extract_pdf_pages.main import compile_final_signed_operating_agreement
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.integration
def test_compile_final_signed_operating_agreement():
    # Set up paths to real test data
    test_data_dir = Path(__file__).parent / "test_data"
    clean_oa_filename = os.environ.get("CLEAN_OA_FILENAME")
    assert clean_oa_filename, "CLEAN_OA_FILENAME environment variable not set"
    print(f"Using clean OA filename: {clean_oa_filename}")
    clean_oa = test_data_dir / clean_oa_filename
    signed_dir = test_data_dir / "Indiv"

    # Choose signature page numbers for test (adjust as appropriate for your test data)
    investor_sig_page_number = 28
    manager_sig_page_number = 27

    result_pdf = compile_final_signed_operating_agreement(
        clean_oa_path=clean_oa,
        investor_signed_oas_dir=signed_dir,
        investor_sig_page_number=investor_sig_page_number,
        manager_sig_page_number=manager_sig_page_number,
    )

    # Check result exists
    assert result_pdf.exists()
    # Optionally, check number of pages or other properties
    with open(result_pdf, "rb") as f:
        reader = PdfReader(f)

        expected_pages = 44  # Adjust based on your test data
        assert len(reader.pages) == expected_pages
