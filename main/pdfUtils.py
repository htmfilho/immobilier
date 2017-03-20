__author__ = 'verpoorten'

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

def pdf_batiment1(modeladmin, request, queryset):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


#----------------------------------------------------------------------
def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawRightString(200*mm, 20*mm, text)

#----------------------------------------------------------------------
def pdf_batiment(modeladmin, request, queryset):
    """
    Create a multi-page document
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,pagesize=letter,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story = []

    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    full_name = "Marvin Jones"
    address_parts = ["411 State St.", "Reno, NV 80158"]

    for page in range(5):
        # Create return address
        ptext = '<font size=12>%s</font>' % full_name
        Story.append(Paragraph(ptext, styles["Normal"]))
        for part in address_parts:
            ptext = '<font size=12>%s</font>' % part.strip()
            Story.append(Paragraph(ptext, styles["Normal"]))

        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        ptext = """<font size=12>We would like to welcome you to our subscriber base
        for %s Magazine! You will receive %s issues at the excellent introductory
        price of $%s. Please respond by %s to start receiving your subscription
        and get the following free gift: %s.</font>"""
        ptext = ptext % (magName, issueNum, subPrice, limitedDate, freeGift)
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))


        ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Sincerely,</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 48))
        ptext = '<font size=12>Ima Sucker</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        Story.append(PageBreak())

    doc.build(Story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

