from pathlib import Path
from typing import Union, Optional, List, Sequence
from pypdf import PdfReader, PdfWriter
import typer

app = typer.Typer(
    help="PDF extraction and combination utilities for operating agreements."
)


def extract_same_page_from_pdfs(
    input_file_dir_arg: Union[Path, str],
    page_number_to_extract_arg: int = 0,
    output_file_dir_arg: str = "Investor Sig Pages",
    output_file_name_prefix_arg: str = "Sig Page - ",
) -> Path:
    """Extracts a single page from a directory of PDFs and saves the extracted pages to a new directory.
    Useful for extracting signature pages from a directory of individually signed operating agreements.

    input_file_dir_arg: Path or str - the directory containing the PDFs to extract pages from
    page_number_to_extract_arg: int - the zero-indexed page number to extract (default: 0)
    output_file_dir_arg: str - the name of the directory to save the extracted pages to (default: "extracted_pages")
    output_file_name_prefix: str - the prefix to add to the output file names (default: "Sig Page - ")
    """

    # Argument validation
    input_file_dir = Path(input_file_dir_arg)
    output_file_dir = input_file_dir.parent / output_file_dir_arg
    page_number_to_extract = page_number_to_extract_arg
    output_file_name_prefix = output_file_name_prefix_arg

    print("Input file directory: " + str(input_file_dir))
    print("Output file directory: " + str(output_file_dir))
    print("Output file name prefix: " + output_file_name_prefix)
    print(
        "Page number to extract: "
        + str(page_number_to_extract)
        + f" (PDF page {page_number_to_extract + 1})\n"
    )

    # create output directory if it doesn't exist
    if not output_file_dir.exists():
        output_file_dir.mkdir(parents=True, exist_ok=True)
        print("Created: " + str(output_file_dir))

    # iterate through input files (sorted for consistency)
    print("Starting PDF extraction...")
    print("Extracting page " + str(page_number_to_extract) + " from PDFs...")
    for input_file_full_path in sorted(input_file_dir.glob("*.pdf")):
        try:
            with open(input_file_full_path, "rb") as f:
                input_file = PdfReader(f)
                output_file = PdfWriter()
                # check if page exists
                if page_number_to_extract < 0 or page_number_to_extract >= len(
                    input_file.pages
                ):
                    print(f"Skipped (page out of range): {input_file_full_path}")
                    continue
                page = input_file.pages[page_number_to_extract]
                output_file.add_page(page)
                output_file_full_path = output_file_dir / (
                    output_file_name_prefix + input_file_full_path.name
                )
                with open(output_file_full_path, "wb") as output_stream:
                    output_file.write(output_stream)
                print("Created: " + str(output_file_full_path))
        except Exception as e:
            print(f"Error processing {input_file_full_path}: {e}")

    print("\nPDF extraction complete.")

    return output_file_dir


def combine_pdfs_in_dir(
    input_file_dir_arg: Union[Path, str],
    output_file_dir_arg: Optional[str] = None,
    output_file_name_arg: str = "Investor Sig Pages Combined.pdf",
) -> Path:
    """Combines a directory of PDFs into a single PDF.
    Useful for combining signature pages into a single PDF.

    input_file_dir_arg: Path or str - the directory containing the PDFs to combine
    output_file_dir_arg: str or None - the name of the directory to save the combined PDF to (default: None)
    output_file_name_arg: str - the name of the combined PDF file (default: "Combined.pdf")
    """

    # Argument validation
    input_file_dir = Path(input_file_dir_arg)
    if output_file_dir_arg is None:
        output_file_dir = input_file_dir.parent
    else:
        output_file_dir = input_file_dir.parent / output_file_dir_arg
    output_file_name = output_file_name_arg

    print("Input file directory: " + str(input_file_dir))
    print("Output file directory: " + str(output_file_dir))
    print("Output file name: " + output_file_name + "\n")

    # create output directory if it doesn't exist
    if not output_file_dir.exists():
        output_file_dir.mkdir(parents=True, exist_ok=True)
        print("Created: " + str(output_file_dir))

    output_file = PdfWriter()

    # iterate through input files (sorted for consistency)
    print("Starting PDF combination...")
    print("Combining PDFs...")
    for input_file_full_path in sorted(input_file_dir.glob("*.pdf")):
        try:
            with open(input_file_full_path, "rb") as f:
                input_file = PdfReader(f)
                for page in input_file.pages:
                    output_file.add_page(page)
            print("Added: " + str(input_file_full_path))
        except Exception as e:
            print(f"Error processing {input_file_full_path}: {e}")

    # write output file to disk
    output_file_full_path = output_file_dir / output_file_name
    with open(output_file_full_path, "wb") as output_stream:
        output_file.write(output_stream)

    print("Created: " + str(output_file_full_path))
    print("\nPDF combination complete.")

    return output_file_full_path


def slice_pdf(
    input_file_path: Union[Path, str],
    start_page: int = 0,
    end_page: int = -1,
    output_file_dir_arg: Optional[str] = None,
    output_file_name_arg: str = "Sliced.pdf",
) -> Path:
    """Slices a PDF into a new PDF.
    Useful for slicing a PDF into a single page PDF.

    input_file_path: Path or str - the path to the PDF to slice
    start_page: int - the zero-indexed page number to start slicing from (default: 0)
    end_page: int - the zero-indexed page number to end slicing at (non-inclusive) (default: 1)
    output_file_dir_arg: str or None - the name of the subdirectory to save the sliced PDF to (default: None)
    output_file_name_arg: str - the name of the sliced PDF file (default: "Sliced.pdf")
    """

    # Argument validation
    input_file_path = Path(input_file_path)
    if output_file_dir_arg is None:
        output_file_dir = input_file_path.parent
    else:
        output_file_dir = input_file_path.parent / output_file_dir_arg
    output_file_name = output_file_name_arg

    print("Input file path: " + str(input_file_path))
    print("Output file directory: " + str(output_file_dir))
    print("Output file name: " + output_file_name + "\n")

    # create output directory if it doesn't exist
    if not output_file_dir.exists():
        output_file_dir.mkdir(parents=True, exist_ok=True)
        print("Created: " + str(output_file_dir))

    output_file = PdfWriter()

    # open input file
    with open(input_file_path, "rb") as f:
        input_file = PdfReader(f)
        num_pages = len(input_file.pages)
        # handle end_page == -1 as "to the end"
        if end_page == -1 or end_page is None:
            end_page_actual = num_pages
        else:
            end_page_actual = end_page
        # clamp start_page and end_page_actual to valid range
        start_page = max(0, start_page)
        end_page_actual = min(num_pages, end_page_actual)
        for page in input_file.pages[start_page:end_page_actual]:
            output_file.add_page(page)

    # write output file to disk
    output_file_full_path = output_file_dir / output_file_name
    with open(output_file_full_path, "wb") as output_stream:
        output_file.write(output_stream)

    print("Created: " + str(output_file_full_path))
    print("\nPDF slicing complete.")

    return output_file_full_path


def combine_pdfs_from_list(
    input_file_list_arg: Sequence[Union[str, Path]],
    output_file_dir_arg: Union[str, Path],
    output_file_name_arg: str = "Combined.pdf",
) -> Path:
    """Combines a list of PDFs into a single PDF.
    Useful for combining signature pages into a single PDF.

    input_file_list_arg: list - the list of PDFs to combine
    output_file_dir_arg: str or Path - the name of the subdirectory to save the combined PDF to
    output_file_name_arg: str - the name of the combined PDF file (default: "Combined.pdf")
    """

    # Argument validation
    input_file_list = [Path(f) for f in input_file_list_arg]
    output_file_dir = Path(output_file_dir_arg)
    output_file_name = output_file_name_arg

    print("Input file list: " + str(input_file_list))
    print("Output file directory: " + str(output_file_dir))
    print("Output file name: " + output_file_name + "\n")

    # create output directory if it doesn't exist
    if not output_file_dir.exists():
        output_file_dir.mkdir(parents=True, exist_ok=True)
        print("Created: " + str(output_file_dir))

    output_file = PdfWriter()

    # iterate through input files
    print("Starting PDF combination...")
    print("Combining PDFs...")
    for input_file_full_path in input_file_list:
        try:
            with open(input_file_full_path, "rb") as f:
                input_file = PdfReader(f)
                for page in input_file.pages:
                    output_file.add_page(page)
            print("Added: " + str(input_file_full_path))
        except Exception as e:
            print(f"Error processing {input_file_full_path}: {e}")

    # write output file to disk
    output_file_full_path = output_file_dir / output_file_name
    with open(output_file_full_path, "wb") as output_stream:
        output_file.write(output_stream)

    print("Created: " + str(output_file_full_path))
    print("\nPDF combination complete.")

    return output_file_full_path


def compile_final_signed_operating_agreement(
    clean_oa_path: Union[Path, str],
    investor_signed_oas_dir: Union[Path, str],
    investor_sig_page_number: int,
    manager_sig_page_number: int,
    output_file_name: Optional[str] = None,
) -> Path:
    """Compiles a final signed operating agreement from a clean operating agreement and a directory of signed operating agreements.
    Useful for compiling a final signed operating agreement from a directory of individually signed operating agreements.

    clean_oa_path: Path or str - the path to the clean operating agreement
    investor_signed_oas_dir: Path or str - the directory containing the signed operating agreements
    investor_sig_page_number: int - the zero-indexed page number of the investor signature page
    manager_sig_page_number: int - the zero-indexed page number of the manager signature page
    """

    # Argument validation
    clean_oa_path = Path(clean_oa_path)
    investor_signed_oas_dir = Path(investor_signed_oas_dir)

    print("Clean operating agreement path: " + str(clean_oa_path))
    print(
        "Investor signed operating agreements directory: "
        + str(investor_signed_oas_dir)
    )
    print(
        "Investor signature page number: "
        + str(investor_sig_page_number)
        + f" (PDF page {investor_sig_page_number + 1})"
    )
    print(
        "Manager signature page number: "
        + str(manager_sig_page_number)
        + f" (PDF page {manager_sig_page_number + 1})\n"
    )

    # extract signature pages from PDFs
    sig_pages_output_dir = extract_same_page_from_pdfs(
        investor_signed_oas_dir,
        investor_sig_page_number,
    )

    # combine signature pages into a single PDF
    combined_sig_pages_path = combine_pdfs_in_dir(sig_pages_output_dir)

    # extract pages before signature pages from clean operating agreement
    oa_beginning_path = slice_pdf(
        clean_oa_path,
        0,
        min(investor_sig_page_number, manager_sig_page_number),
        output_file_dir_arg=None,
        output_file_name_arg="OA Beginning.pdf",
    )

    # extract pages after signature pages from clean operating agreement
    oa_ending_path = slice_pdf(
        clean_oa_path,
        max(investor_sig_page_number, manager_sig_page_number) + 1,
        -1,
        output_file_dir_arg=None,
        output_file_name_arg="OA Ending.pdf",
    )

    # extract manager signature page from clean operating agreement
    manager_sig_page_path = slice_pdf(
        clean_oa_path,
        manager_sig_page_number,
        manager_sig_page_number + 1,
        output_file_dir_arg=None,
        output_file_name_arg="Manager Signature Page.pdf",
    )

    # combine clean operating agreement pages with signature pages
    doc_components_list = []
    if manager_sig_page_number < investor_sig_page_number:
        doc_components_list = [
            oa_beginning_path,
            manager_sig_page_path,
            combined_sig_pages_path,
            oa_ending_path,
        ]
    else:
        doc_components_list = [
            oa_beginning_path,
            combined_sig_pages_path,
            manager_sig_page_path,
            oa_ending_path,
        ]

    # combine all components into final PDF
    if output_file_name is None:
        output_file_name = clean_oa_path.stem + " FINAL COMBINED.pdf"

    combined_pdf_path = combine_pdfs_from_list(
        doc_components_list,
        output_file_dir_arg=clean_oa_path.parent,
        output_file_name_arg=output_file_name,
    )

    print("Final Combined PDF: " + str(combined_pdf_path) + "\n")

    return combined_pdf_path


@app.command()
def extract(
    input_dir: Path = typer.Argument(
        ..., help="Directory containing PDFs to extract from."
    ),
    page_number: int = typer.Option(0, help="Zero-indexed page number to extract."),
    sig_pages_output_dir: str = typer.Option(
        "Sig Pages", help="Directory to save extracted pages."
    ),
    output_prefix: str = typer.Option(
        "Sig Page - ", help="Prefix for output file names."
    ),
):
    """Extract a single page from each PDF in a directory."""
    extract_same_page_from_pdfs(
        input_file_dir_arg=input_dir,
        page_number_to_extract_arg=page_number,
        output_file_dir_arg=sig_pages_output_dir,
        output_file_name_prefix_arg=output_prefix,
    )


@app.command()
def combine(
    input_dir: Path = typer.Argument(..., help="Directory containing PDFs to combine."),
    sig_pages_output_dir: Optional[str] = typer.Option(
        None, help="Directory to save the combined PDF."
    ),
    output_name: str = typer.Option(
        "Sig Pages Combined.pdf", help="Name of the combined PDF."
    ),
):
    """Combine all PDFs in a directory into a single PDF."""
    combine_pdfs_in_dir(
        input_file_dir_arg=input_dir,
        output_file_dir_arg=sig_pages_output_dir,
        output_file_name_arg=output_name,
    )


@app.command()
def slice(
    input_file: Path = typer.Argument(..., help="PDF file to slice."),
    start_page: int = typer.Option(0, help="Zero-indexed start page."),
    end_page: int = typer.Option(
        1, help="Zero-indexed end page (non-inclusive, -1 for end)."
    ),
    sig_pages_output_dir: Optional[str] = typer.Option(
        None, help="Directory to save the sliced PDF."
    ),
    output_name: str = typer.Option("Sliced.pdf", help="Name of the sliced PDF."),
):
    """Slice a PDF into a new PDF containing a range of pages."""
    slice_pdf(
        input_file_path=input_file,
        start_page=start_page,
        end_page=end_page,
        output_file_dir_arg=sig_pages_output_dir,
        output_file_name_arg=output_name,
    )


@app.command()
def combine_list(
    input_files: List[Path] = typer.Argument(..., help="List of PDF files to combine."),
    sig_pages_output_dir: Path = typer.Argument(
        ..., help="Directory to save the combined PDF."
    ),
    output_name: str = typer.Option("Combined.pdf", help="Name of the combined PDF."),
):
    """Combine a list of PDFs into a single PDF."""
    combine_pdfs_from_list(
        input_file_list_arg=input_files,
        output_file_dir_arg=sig_pages_output_dir,
        output_file_name_arg=output_name,
    )


@app.command()
def compile_final(
    clean_oa: Path = typer.Argument(
        ..., help="Path to the clean operating agreement PDF."
    ),
    signed_dir: Path = typer.Argument(
        ..., help="Directory containing signed operating agreements."
    ),
    investor_sig_page: int = typer.Argument(
        ..., help="Zero-indexed page number of investor signature."
    ),
    manager_sig_page: int = typer.Argument(
        ..., help="Zero-indexed page number of manager signature."
    ),
):
    """Compile a final signed operating agreement from a clean OA and signed OAs."""
    compile_final_signed_operating_agreement(
        clean_oa_path=clean_oa,
        investor_signed_oas_dir=signed_dir,
        investor_sig_page_number=investor_sig_page,
        manager_sig_page_number=manager_sig_page,
    )
