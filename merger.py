import PyPDF2

class PDFMerger:
    def __init__(self):
        self.merger = PyPDF2.PdfMerger()

    def add_files(self, pdf_files):
        for pdf in pdf_files:
            self.merger.append(pdf)

    def save(self, output_path="PDF_Mesclado.pdf"):
        self.merger.write(output_path)
        self.merger.close()
        return output_path
