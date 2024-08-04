import os
import pdfplumber

from constants.location import PDF_CACHE_DIR


class PdfParser:
    """
    Parses input PDF file for text and embedded images
    """

    def __init__(self, pdf_name: str) -> None:
        """
        Initializes the class
        :param pdf_name: name of PDF file to be processed
        """
        self.text = ""
        self.images = []
        self._pdf_path = os.path.join(PDF_CACHE_DIR, pdf_name)

        self._parse_pdf()

    def _parse_pdf(self) -> None:
        """
        Performs parsing operations to retrieve text and images of PDF source
        """
        with pdfplumber.open(self._pdf_path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text()
                for image in page.images:
                    self.images.append(image)
