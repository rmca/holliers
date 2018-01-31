from pyPdf import PdfFileWriter, PdfFileReader
from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def overlay_text_at_loc_on_pdf(text, loc, existing_pdf, output_pdf):
    # create a new PDF with Reportlab
    packet = StringIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(loc[0],loc[1], text)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(existing_pdf)
    # read your existing PDF
    output = PdfFileWriter()
    page = new_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    output.write(output_pdf)

with open('newpdf2.pdf', 'wb') as fp:
    overlay_text_at_loc_on_pdf("Robert McAdoo", (160, 650,), file('holidays.pdf', 'rb'), fp)
