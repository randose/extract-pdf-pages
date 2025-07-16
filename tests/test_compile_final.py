from pathlib import Path
from shutil import copytree, copy2
from pypdf import PdfReader
import os
import pytest

from extract_pdf_pages.main import compile_final_signed_operating_agreement
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.integration
def test_compile_final_signed_operating_agreement(tmp_path: Path):
    """
    Integration test that runs the compile_final_signed_operating_agreement function using a set of test data
    consisting of a clean operating agreement and a directory of signed operating agreements.

    Steps
    -----
    1. Copy test_data/* → tmp_path/
    2. Invoke compile_final_signed_operating_agreement with paths
       pointing into tmp_path.
    3. Assert the output PDF exists and has the expected page count.
    4. tmp_path is automatically deleted by pytest afterwards.
    """

    source_data_dir = Path(__file__).parent / "test_data"

    # Copy test data to a temporary directory
    for item in source_data_dir.iterdir():
        dest = tmp_path / item.name
        if item.is_dir():
            copytree(item, dest)
        else:
            copy2(item, dest)

    clean_oa_filename = os.environ.get("CLEAN_OA_FILENAME")
    assert clean_oa_filename, "CLEAN_OA_FILENAME environment variable not set"
    print(f"Using clean OA filename: {clean_oa_filename}")

    clean_oa = tmp_path / clean_oa_filename
    signed_dir = tmp_path / "Indiv"

    # Signature pages for this fixture set
    investor_sig_page_number = 28
    manager_sig_page_number = 27

    result_pdf = compile_final_signed_operating_agreement(
        clean_oa_path=clean_oa,
        investor_signed_oas_dir=signed_dir,
        investor_sig_page_number=investor_sig_page_number,
        manager_sig_page_number=manager_sig_page_number,
    )

    # Check result exists
    assert result_pdf.exists(), "Result PDF was not created"

    # Check the number of pages in the result PDF
    with open(result_pdf, "rb") as f:
        reader = PdfReader(f)
        expected_pages = 44  # Adjust if fixture changes
        assert len(reader.pages) == expected_pages
