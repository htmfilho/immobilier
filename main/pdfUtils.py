##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

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


def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawRightString(200*mm, 20*mm, text)


def pdf_batiment(modeladmin, request, queryset):
    response = set_response()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = set_styles()

    Story = []

    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    full_name = "Marvin Jones"
    address_parts = ["411 State St.", "Reno, NV 80158"]

    for page in range(5):
        create_page(Story, address_parts, freeGift, full_name, issueNum, limitedDate, magName, styles, subPrice)

    doc.build(Story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def create_page(Story, address_parts, freeGift, full_name, issueNum, limitedDate, magName, styles, subPrice):
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


def set_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    return styles


def set_response():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    return response

