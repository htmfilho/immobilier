from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import sys

from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus import NextPageTemplate, Paragraph, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch
from reportlab.graphics import renderPDF

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
PAGE_WIDTH,PAGE_HEIGHT = A4
def create_pdf():
    input_file = "chat.pdf"
    output_file = "my_file_with_footer.pdf"

    # Get pages
    reader = PdfReader(input_file)
    pages = [pagexobj(p) for p in reader.pages]


    # Compose new pdf
    canvas = Canvas(output_file)
    for page_num, page in enumerate(pages, start=1):
        x = 0
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        lien = '<link href="#%s" color="red">is a link to %s</link>'% (page_num,page_num)
        canvas.drawString(page.BBox[0]-x, 65, lien)
        canvas.restoreState()

        canvas.showPage()

    for page_num, page in enumerate(pages, start=1):

        # Add page
        canvas.setPageSize((page.BBox[2], page.BBox[3]))
        canvas.doForm(makerl(canvas, page))
        ancre = '<a name="%s"></a>' % page_num

        canvas.drawString(page.BBox[0]-x, 65, ancre)
        # Draw footer
        footer_text = "Page %s of %s" % (page_num, len(pages))
        x = 128
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(0.5)
        canvas.line(66, 78, page.BBox[2] - 66, 78)
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(page.BBox[2]-x, 65, footer_text)
        canvas.restoreState()

        canvas.showPage()

    canvas.save()


if __name__ == '__main__':
    create_pdf()
