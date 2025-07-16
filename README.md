# Extract PDF Pages

A command-line tool for extracting, slicing, and combining pages from PDF files, designed for workflows involving operating agreements and signature pages. Built with [Typer](https://typer.tiangolo.com/).

## Features

- **Extract** a specific page from every PDF in a directory.
- **Combine** all PDFs in a directory into a single PDF.
- **Slice** a PDF to extract a range of pages.
- **Combine List** of arbitrary PDF files into one.
- **Compile Final** signed operating agreement from a clean OA and a directory of signed OAs.

## 🚀 Installation

1. Clone this repository and navigate to the project directory.
2. Install dependencies and build the package [Poetry](https://python-poetry.org/):

   ```sh
   poetry install
   poetry build
   ```

3. Install globally with [pipx](https://pypa.github.io/pipx/):

   ```sh
   pipx install dist/extract_pdf_pages_cli-*.whl
   ```

   *(Replace `extract_pdf_pages-*.whl` with the actual wheel filename if needed.)*

## Usage

```sh
extract-pdf-pages [COMMAND] [OPTIONS]
```

### Commands

#### Extract

Extract a single page from each PDF in a directory.

```sh
extract-pdf-pages extract [INPUT_DIR] --page-number 0 --output-dir "Sig Pages" --output-prefix "Sig Page - "
```

#### Combine

Combine all PDFs in a directory into a single PDF.

```sh
extract-pdf-pages combine [INPUT_DIR] --output-dir [OUTPUT_DIR] --output-name "Combined.pdf"
```

#### Slice

Slice a PDF into a new PDF containing a range of pages.

```sh
extract-pdf-pages slice [INPUT_FILE] --start-page 0 --end-page -1 --output-dir [OUTPUT_DIR] --output-name "Sliced.pdf"
```

#### Combine List

Combine a list of PDFs into a single PDF.

```sh
extract-pdf-pages combine-list [INPUT_FILE1] [INPUT_FILE2] ... [OUTPUT_DIR] --output-name "Combined.pdf"
```

#### Compile Final

Compile a final signed operating agreement from a clean OA and signed OAs.

```sh
extract-pdf-pages compile-final [CLEAN_OA] [SIGNED_DIR] [INVESTOR_SIG_PAGE] [MANAGER_SIG_PAGE]
```

## 📂 Example

Extract page 28 from all PDFs in `Signed Individual` and combine them:

```sh
extract-pdf-pages extract "Signed Individual" --page-number 28
extract-pdf-pages combine "Signed Individual/Sig Pages"
```

## 🛠 License

MIT License.
