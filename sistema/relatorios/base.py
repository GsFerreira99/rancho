from PyPDF2 import PdfFileWriter, PdfFileReader
import io

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class Pdf:

    def __init__(self, modelo: str) -> None:
        self.modelo = modelo
        self.packet = io.BytesIO()
        self.can = canvas.Canvas(self.packet, pagesize=letter)

    def criar_pdf(self):
        self.packet.seek(0)
        self.new_pdf = PdfFileWriter()
        self.dados = PdfFileReader(self.packet)
        self.existing_pdf = PdfFileReader(open(self.modelo, "rb"))

        self.new_pdf.addPage(self.existing_pdf.getPage(0))
        self.new_pdf.getPage(0).mergePage(self.dados.getPage(0))

        self.new_pdf.write(self.packet)
        return self.packet.getvalue()

    def close(self):
        return self.packet.close()

    def get_value(self):
        return self.new_pdf
