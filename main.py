from pathlib import Path
from typing import Union
from pypdf import PdfReader, PdfWriter


def extract_same_page_from_pdfs(
    input_file_dir_arg: Union[Path, str],
    page_number_to_extract_arg: int = 0,
    output_file_dir_arg: str = "Sig Pages",
    output_file_name_prefix_arg: str = "Sig Page - ",
):
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
    output_file_dir_arg: Union[str, None] = None,
    output_file_name_arg: str = "Sig Pages Combined.pdf",
):
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
    end_page: int = 1,
    output_file_dir_arg: Union[str, None] = None,
    output_file_name_arg: str = "Sliced.pdf",
):
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
    input_file_list_arg: list,
    output_file_dir_arg: Union[str, Path],
    output_file_name_arg: str = "Combined.pdf",
):
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
):
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
    output_dir = extract_same_page_from_pdfs(
        investor_signed_oas_dir,
        investor_sig_page_number,
    )

    # combine signature pages into a single PDF
    combined_sig_pages_path = combine_pdfs_in_dir(output_dir)

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

    # combine clean operating agreement pages with signature pages
    combined_pdf_path = combine_pdfs_from_list(
        [oa_beginning_path, combined_sig_pages_path, oa_ending_path],
        output_file_dir_arg=clean_oa_path.parent,
        output_file_name_arg="Operating Agreement FINAL COMBINED.pdf",
    )

    print("Final Combined PDF: " + str(combined_pdf_path) + "\n")

    return combined_pdf_path


if __name__ == "__main__":
    clean_oa_path = r"C:\Users\daniel\Downloads\Operating Agreement - Clean.pdf"
    investor_signed_oas_dir = r"C:\Users\daniel\Downloads\Signed Individual"
    investor_sig_page_number = 28
    manager_sig_page_number = 27

    combined_pdf_path = compile_final_signed_operating_agreement(
        clean_oa_path,
        investor_signed_oas_dir,
        investor_sig_page_number,
        manager_sig_page_number,
    )
