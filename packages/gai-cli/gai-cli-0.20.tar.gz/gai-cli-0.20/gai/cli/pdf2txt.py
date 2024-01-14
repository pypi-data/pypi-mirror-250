import sys
from unstructured.partition.pdf import partition_pdf
import re
from gai.tools.PDFConvert import PDFConvert

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        raise ValueError("No input provided. Please provide input either via stdin or as a command line argument.")
    pdf_file_path = args[0]
    print(PDFConvert.pdf_to_text(pdf_file_path, clean=False))

if __name__ == "__main__":
    main()