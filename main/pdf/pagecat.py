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
from django.shortcuts import render
from django.views.generic import *

from reportlab.platypus import Paragraph

from reportlab.lib.styles import ParagraphStyle

from reportlab.platypus.tableofcontents import TableOfContents


def pagecat(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]
    #

    Story = []

    centered = ParagraphStyle(name='centered',
                              fontSize=30,
                              leading=16,
                              alignment=1,
                              spaceAfter=20)

    h1 = ParagraphStyle(
        name='Heading1',
        fontSize=14,
        leading=16)

    h2 = ParagraphStyle(name='Heading2',
                        fontSize=12,
                        leading=14)

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(fontName='Times-Bold', fontSize=20, name='TOCHeading1', leftIndent=20,
                       firstLineIndent=-20, spaceBefore=10, leading=16),
        ParagraphStyle(fontSize=18, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
    ]
    Story.append(toc)
    manual_toc = True
    if manual_toc:
        cpt = 0
        Story.append(Paragraph('<b>Table of contents</b>', centered))
        for fname in pdfs:
            Story.append(Paragraph('<includePdfPages filename="%s" pages="1" outlineText="crasher"/>' % fname, h1))

            Story.append(Paragraph('%s' % fname, h2))
            cpt = cpt + 1
    doc = MyDocTemplate('mintoc.pdf')

    doc.multiBuild(Story)
    return render(request, "test.html")

def mainPageFrame(canvas, doc):
    """The page frame used for all PDF documents."""

    canvas.saveState()

    pageNumber = canvas.getPageNumber()
    canvas.line(2*cm, A4[1]-2*cm, A4[0]-2*cm, A4[1]-2*cm)
    canvas.line(2*cm, 2*cm, A4[0]-2*cm, 2*cm)
    if pageNumber > 1:
        canvas.setFont('Times-Roman', 12)
        canvas.drawString(4 * inch, cm, "%d" % pageNumber)
        if hasattr(canvas, 'headerLine'):  # hackish
            headerline = ' \xc2\x8d '.join(canvas.headerLine)
            canvas.drawString(2*cm, A4[1]-1.75*cm, headerline)

    canvas.setFont('Times-Roman', 8)
    msg = "Generated with docpy. See http://www.reportlab.com!"
    canvas.drawString(2*cm, 1.65*cm, msg)

    canvas.restoreState()



class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        frame1 = Frame(2.5*cm, 2.5*cm, 15*cm, 25*cm, id='F1')
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        self.addPageTemplates(PageTemplate('normal', [frame1], mainPageFrame))

    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
