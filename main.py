from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def overlay_text_at_loc_on_pdf(texts, original_pdf, output_pdf):
    packet = StringIO.StringIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    for text, loc in texts:
    	can.drawString(loc[0], loc[1], text)
    can.save()

    #move to the beginning of the StringIO buffer
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
   

texts = [
	("Robert McAdoo", (130, 640,),),
	("Nicola Asuni", (130, 620,),),
	("x", (45, 545,),),
	("20 days", (295, 475,),),
	("From date", (205, 425,),),
	("To date", (405, 425,),),
]


import click
from click_datetime import Datetime


@click.group()
def cli():
    pass

def make_form_content(name, manager, num_days, from_date, to_date):
    return [
        (name, (130, 640,),),
        (manager, (130, 620,),),
        ("x", (45, 545,),),
        ("{} days".format(num_days), (295, 475,),),
        (from_date, (205, 425,),),
        (to_date, (405, 425,),),
    ] 

@click.command()
@click.argument('name', type=str, required=True)
@click.argument('manager', type=str, required=True)
@click.argument('num_days', type=int, required=True)
@click.argument('from_date', type=Datetime(format='%d/%m/%y'), required=True)
@click.argument('to_date', type=Datetime(format='%d/%m/%y'), required=True)
@click.option('--output-file', type=click.Path(exists=False), default='holiday_request.pdf')
@click.option('--template-file', type=click.Path(exists=True), default='holidays.pdf')
def holiday(name, manager, num_days, from_date, to_date, output_file, template_file):
    """
    Holidays for the lazy.

    Fills out a holiday request form on your behalf so you don't have to.
    """
    texts = make_form_content(name, manager, num_days, from_date.strftime('%d/%m/%y'), to_date.strftime('%d/%m/%y'))
    overlay_text_at_loc_on_pdf(texts, template_file, output_file)


@click.command()
@click.option('--form-file', default='holida_request.pdf')
def show(ctx, form_file):
    pass 

cli.add_command(holiday)

if __name__ == '__main__':
    cli({})
