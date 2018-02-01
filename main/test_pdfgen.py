from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
PAGE_WIDTH, PAGE_HEIGHT = A4


def create_pdf():
    reader = PdfReader("chat.pdf")
    pages = [pagexobj(p) for p in reader.pages]

    canvas = Canvas("my_file_with_footer.pdf")
    for page_num, page in enumerate(pages, start=1):
        x = 0
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        lien = '<link href="#%s" color="red">is a link to %s</link>' % (page_num, page_num)
        canvas.drawString(page.BBox[0]-x, 65, lien)
        canvas.restoreState()

        canvas.showPage()

    create_pages(canvas, pages, x)

    canvas.save()


def create_pages(canvas, pages, x):
    for page_num, page in enumerate(pages, start=1):
        canvas.setPageSize((page.BBox[2], page.BBox[3]))
        canvas.doForm(makerl(canvas, page))
        ancre = '<a name="%s"></a>' % page_num

        canvas.drawString(page.BBox[0] - x, 65, ancre)

        footer_text = "Page %s of %s" % (page_num, len(pages))
        x = 128
        canvas.saveState()
        canvas.setStrokeColorRGB(0, 0, 0)
        canvas.setLineWidth(0.5)
        canvas.line(66, 78, page.BBox[2] - 66, 78)
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(page.BBox[2] - x, 65, footer_text)
        canvas.restoreState()

        canvas.showPage()


if __name__ == '__main__':
    create_pdf()
