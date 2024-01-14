import pypdfium2 as pdfium
from pypdf2 import PdfMerger

class AutoPdf():
    """
    A class to automate PDF operations.
    """

    def __init__(self):
        self.file = None

    def open_pdf(self, Path: str) -> pdfium.PdfDocument:
        """
        Open a PDF file.

        :param Path: The path of the PDF file to open.
        :return: The opened PDF file.
        """
        self.file = pdfium.PdfDocument(Path)
        return self.file
    
    def page_count(self, file: pdfium.PdfDocument) -> int:
        """
        Get the number of pages in a PDF file.

        :param file: The PDF file.
        :return: The number of pages in the PDF file.
        """
        page_count = len(file)
        return page_count
    
    def pdf_page_to_img(self, file: pdfium.PdfDocument) -> None:
        """
        Convert each page of a PDF file to an image.

        :param file: The PDF file.
        """
        n_pages = len(file)
        for page_number in range(n_pages):
            page = file.get_page(page_number)
            
            pil_image = page.render(
                scale=1,
                rotation=0,
            ).to_pil()
            pil_image.save(f"image_{page_number+1}.png")
    

    def split_pages(self, file: pdfium.PdfDocument) -> None:
        """
        Split a PDF file into separate pages.

        :param file: The PDF file.
        """
        n_pages = len(file)
        for page_number in range(n_pages):
            page =file.get_page(page_number)

            page.save(f"pdf_{page_number+1}.pdf",version=17)
    

    def merge_pdf(self, files: list) -> None:
        """
        Merge multiple PDF files into one.

        :param files: A list of paths of the PDF files to merge.
        """
        merger = PdfMerger()
        for file in files:
            merger.append(open(file,'rb'))
        merger.write('merged.pdf')
    
    def rotate_pdf(self, file: pdfium.PdfDocument) -> None:
        """
        Rotate a PDF file.

        :param file: The PDF file.
        """
        pass
