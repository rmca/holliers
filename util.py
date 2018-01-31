import StringIO
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def overlay_text_at_loc_on_pdf(texts, original_pdf, output_pdf):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    for text, loc in texts:
        can.drawString(loc[0], loc[1], text)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(file(original_pdf, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = file(output_pdf, "wb")
    output.write(outputStream)
    outputStream.close()


def make_form_content(name, manager, num_days, from_date, to_date):
    return [
        (name, (130, 640,),),
        (manager, (130, 620,),),
        ("x", (45, 545,),),
        ("{} days".format(num_days), (295, 475,),),
        (from_date, (205, 425,),),
        (to_date, (405, 425,),),
    ]

