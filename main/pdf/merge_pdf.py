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

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from PyPDF2 import PdfFileMerger,  PdfFileReader

from reportlab.lib.pagesizes import A4 as A4

PAGE_SIZE = A4
MARGIN_SIZE = 15 * mm
COLS_WIDTH = [20*mm, 55*mm, 45*mm, 15*mm, 40*mm]
STUDENTS_PER_PAGE = 24
BOTTOM_MARGIN = 18
TOP_MARGIN = 85


def merge(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]
    #
    buffer = BytesIO()

    doc = MyDocTemplateMerge(buffer,
                             pagesize=PAGE_SIZE,
                             rightMargin=MARGIN_SIZE,
                             leftMargin=MARGIN_SIZE,
                             topMargin=85,
                             bottomMargin=18)

    content = []

    if not pdfs or len(pdfs) < 2:
        exit("Please enter at least two pdfs for merging!")
    no_page = 2
    manual_toc = True
    if manual_toc:
        cpt = 0
        content.append(Paragraph('Table of contents', ParagraphStyle('normal')))
        for fname in pdfs:
            input = PdfFileReader(open(fname, 'rb'))
            number_of_page = input.getNumPages()

            # lien = '<link href="#%s" color="red">is a link to %s</link>'% (fname,fname)
            #
            #
            # content.append(Paragraph('''
            #                         <para>
            #                             %s       %s-%s %s
            #                         </para>
            #                         ''' % (fname,no_page, no_page + number_of_page,lien), ParagraphStyle('normal')))

            content.append(Paragraph('%s          %s-%s' % (fname, no_page, no_page + number_of_page),
                                     ParagraphStyle('normal')))
            # ancre = '<a name="%s"></a>' % fname
            # content.append(Paragraph('''
            #                             %s
            #                         ''' % (ancre), ParagraphStyle('normal')))
            no_page = no_page + number_of_page
            cpt = cpt + 1

    doc.build(content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)  #  ne garnit que la 1iere page
    # doc.build(content, canvasmaker=NumberedCanvas)
    merger = PdfFileMerger()

    merger.setPageMode('/UseOC')
    merger.append(buffer)
    num_page = 1
    no_page = 1
    cpt = 0
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))

        number_of_page = input.getNumPages()
        lien = "lnk2_" + str(no_page)
        lien = fname
        # ancre = '<a name="%s"></a>' % fname
        # content.append(Paragraph('''
        #
        #                             %s
        #
        #                         ''' % (ancre), ParagraphStyle('normal')) )
        merger.append(input, bookmark=lien, import_bookmarks=False)
        # merger.addNamedDestination(lien, num_page)
        # merger.addBookmark(lien,num_page)

        # if cpt==0:
        #     merger.append(input,bookmark=lien, import_bookmarks=False)
        #     doc_length = input.getNumPages()
        #     outline = input.getOutlines()
        #     print(outline)
        #     parent = merger.findBookmark(outline[-1].title)
        # else:
        #     merger.append(input,bookmark=lien, import_bookmarks=False)
        #     sub = merger.addBookmark("SUBBOOKMARK",doc_length,parent)

        num_page = num_page + 1
        no_page = no_page + number_of_page
        cpt = cpt + 1

    output = open("output.pdf", "wb")
    merger.write(output)
    output.close()

    return render(request, "test.html")


def merge_pdf3(request):
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
    manual_toc = True
    if manual_toc:
        cpt = 0

        for fname in pdfs:
            input = PdfFileReader(open(fname, 'rb'))
            number_of_page = input.getNumPages()
            if cpt > 0:
                lien = '<link href="http://uclouvain.be/index4.html" color="blue">is a link to</link>'
            else:
                # lien = '<link href="#%s" color="red">is a link to</link>'% fname
                lien = '<link destination="#%s" color="red">is a link to</link>' % fname
                lien = '<link href="#%s" color="red">is a link to</link>' % fname

            content.append(Paragraph('''
                                    <para>
                                        %s       %s-%s %s
                                    </para>
                                    ''' % (fname, no_page, no_page + number_of_page, lien), ParagraphStyle('normal')))

            # content.append(lien)
            ancre = '<a name="%s"></a>' % fname
            content.append(Paragraph('''
                                        %s
                                    ''' % ancre, ParagraphStyle('normal')))
            cpt = cpt + 1

    doc.build(content)

    merger = PdfFileMerger(buffer)

    #merger.append(buffer)
    num_page = 1
    no_page = 1
    cpt = 0

    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))

        number_of_page = input.getNumPages()
        lien = fname
        # ancre = '<a name="%s"></a>' % fname
        # content.append(Paragraph('''
        #
        #                             %s
        #
        #                         ''' % (ancre), ParagraphStyle('normal')) )
        merger.append(input, bookmark=lien, import_bookmarks=False)
        merger._bookmarkName = lien

        # if cpt==0:
        #     merger.append(input,bookmark=lien, import_bookmarks=False)
        #     doc_length = input.getNumPages()
        #     outline = input.getOutlines()
        #     print(outline)
        #     parent = merger.findBookmark(outline[-1].title)
        # else:
        #     merger.append(input,bookmark=lien, import_bookmarks=False)
        #     sub = merger.addBookmark("SUBBOOKMARK",doc_length,parent)

        num_page = num_page+1
        no_page = no_page + number_of_page
        cpt = cpt+1

    output = open("output.pdf", "wb")

    #merger.write(output)
    #merger.write(doc)
    merger.write(output)
    content.append(Paragraph('''
                                        <para>
                                            %s
                                        </para>
                                        ''' % 'tesrrrrrrrrrrrr t', ParagraphStyle('normal')))
    doc.build(content)
    return render(request, "test.html")


def merge_pdf_stack(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]

    buffer = BytesIO()

    doc = MyDocTemplateMerge(buffer,
                             pagesize=PAGE_SIZE,
                             rightMargin=MARGIN_SIZE,
                             leftMargin=MARGIN_SIZE,
                             topMargin=85,
                             bottomMargin=18)

    content = []

    no_page = 2

    cpt = 0
    content.append(Paragraph('Table of contents', ParagraphStyle('normal')))
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))
        number_of_page = input.getNumPages()
        content.append(Paragraph('%s          %s-%s' % (fname, no_page, no_page + number_of_page),
                                 ParagraphStyle('normal')))
        no_page = no_page + number_of_page
        cpt = cpt + 1

    doc.build(content)
    merger = PdfFileMerger()
    merger.setPageMode('/UseOC')

    num_page = 1
    no_page = 1
    cpt = 0
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))
        number_of_page = input.getNumPages()
        lien = fname
        merger.append(input, bookmark=lien, import_bookmarks=False)
        num_page = num_page + 1
        no_page = no_page + number_of_page
        cpt = cpt + 1

    merger.append(buffer)
    output = open("output.pdf", "wb")
    merger.write(output)
    output.close()

    return render(request, "test.html")


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.restoreState()


class MyDocTemplateMerge(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'normal':
                self.notify('TOCEntry', (0, text, self.page))


def add_header_footer(canvas, doc):
    """
    Add the page number
    """
    styles = getSampleStyleSheet()
    # Save the state of our canvas so we can draw on it
    canvas.saveState()

    # Header
    header_building(canvas, doc, styles)

    # Footer
    footer_building(canvas, doc, styles)

    # Release the canvas
    canvas.restoreState()



def header_building(canvas, doc, styles):
    a = Image(settings.LOGO_URL, width=15*mm, height=20*mm)

    p = Paragraph('''<para align=center>
                        <font size=16>%s</font>
                    </para>''' % (_('scores_transcript')), styles["BodyText"])

    data_header = [[a, '%s' % _('ucl_denom_location'), p], ]

    t_header = Table(data_header, [30*mm, 100*mm, 50*mm])

    t_header.setStyle(TableStyle([]))

    w, h = t_header.wrap(doc.width, doc.topMargin)
    t_header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)



def footer_building(canvas, doc, styles):
    pageinfo = _('scores_sheet')
    footer = Paragraph(''' <para align=right>Page %d - %s </para>''' % (doc.page, pageinfo), styles['Normal'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

#
#
#
#
# class NumberedCanvas(canvas.Canvas):
#     def __init__(self, *args, **kwargs):
#         canvas.Canvas.__init__(self, *args, **kwargs)
#         self._saved_page_states = []
#
#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()
#
#     def save(self):
#         """add page info to each page (page x of y)"""
#         num_pages = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_page_number(num_pages)
#             canvas.Canvas.showPage(self)
#         canvas.Canvas.save(self)
#
#     def draw_page_number(self, page_count):
#         self.setFont("Helvetica", 7)
#         self.drawRightString(200*mm, 20*mm,
#                              "Page %d of %d" % (self._pageNumber, page_count))