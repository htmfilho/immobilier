#############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2017 Verpoorten Leïla
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
from PyPDF2.pdf import RectangleObject
from django.shortcuts import render
from django.views.generic import *

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph

from reportlab.lib.styles import ParagraphStyle
from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.lib.pagesizes import A4 as A4


def merge_pdf4(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=PAGE_SIZE,
                            rightMargin=MARGIN_SIZE,
                            leftMargin=MARGIN_SIZE,
                            topMargin=85,
                            bottomMargin=18)

    content = []

    if not pdfs or len(pdfs) < 2:
        exit("Please enter at least two pdfs for merging!")
    no_page = 1
    legend_text = 'justification_legend'
    legend_text += "<br/><font color=red>%s</font>" % 'fffff'
    p = ParagraphStyle('normal')
    content.append(Paragraph('''
                            <para>
                                %s
                            </para>
                            ''' % legend_text, p))
    doc.build(content)
    items = []
    address = 'WHATEVERYOUWNATTOTYPE'
    address = '<link href="' + 'http://www.hoboes.com/Mimsy/hacks/adding-links-to-pdf/' + '">' + address + '</link>'
    items.append(Paragraph(address, ParagraphStyle('body')))
    doc.multiBuild(items)

    output = PdfFileWriter()

    num_page = 0

    width, height = A4

    output.addBlankPage(width, height)
    cur = 1
    cur_prev = 0
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))

        output.addPage(input.getPage(0))

        output.addBookmark(str(no_page), num_page)
        num_page = num_page + 1
        no_page = no_page + 1

        rect = RectangleObject([400, 400, 600, 600])
        output.addLink(cur_prev, cur, rect)
        cur_prev = cur_prev+1
        cur = cur + 1
    d = open("output.pdf", "wb")

    output.write(d)
    d.close()
    return render(request, "test.html")
