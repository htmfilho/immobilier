#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
usage: platypus_pdf_template.py output.pdf pdf_file_to_use_as_template.pdf

Example of using pdfrw to use a pdf (page one) as the background for all
other pages together with platypus.

There is a table of contents in this example for completeness sake.

"""
import sys

from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus import NextPageTemplate, Paragraph, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
PAGE_WIDTH, PAGE_HEIGHT = A4


class MyTemplate(PageTemplate):
    """The kernel of this example, where we use pdfrw to fill in the
    background of a page before writing to it.  This could be used to fill
    in a water mark or similar."""

    def __init__(self, pdf_template_filename, name=None):
        frames = [Frame(
            0.85 * inch,
            0.5 * inch,
            PAGE_WIDTH - 1.15 * inch,
            PAGE_HEIGHT - (1.5 * inch)
            )]
        PageTemplate.__init__(self, name, frames)
        # use first page as template
        print('pdf_template_filename', pdf_template_filename)
        page = PdfReader(pdf_template_filename).pages[0]
        self.page_template = pagexobj(page)
        # Scale it to fill the complete page
        self.page_xscale = PAGE_WIDTH/self.page_template.BBox[2]
        self.page_yscale = PAGE_HEIGHT/self.page_template.BBox[3]

    def beforeDrawPage(self, canvas, doc):
        """Draws the background before anything else"""
        canvas.saveState()
        rl_obj = makerl(canvas, self.page_template)
        canvas.scale(self.page_xscale, self.page_yscale)
        canvas.doForm(rl_obj)
        canvas.restoreState()


class MyDocTemplate(BaseDocTemplate):
    """Used to apply heading to table of contents."""

    def afterFlowable(self, flowable):
        """Adds Heading1 to table of contents"""
        if flowable.__class__.__name__ == 'Paragraph':
            style = flowable.style.name
            text = flowable.getPlainText()
            key = '%s' % self.seq.nextf('toc')
            if style == 'Heading1':
                self.canv.bookmarkPage(key)
                self.notify('TOCEntry', [1, text, self.page, key])


def create_toc():
    print('createtoc')
    """Creates the table of contents"""
    table_of_contents = TableOfContents()
    table_of_contents.dotsMinLevel = 0
    header1 = ParagraphStyle(name='Heading1', fontSize=16, leading=16)
    header2 = ParagraphStyle(name='Heading2', fontSize=14, leading=14)
    table_of_contents.levelStyles=[header1, header2]

    return [table_of_contents, PageBreak()]


def create_pdf(filename, pdf_template_filename):
    """Create the pdf, with all the contents"""
    print('create_pdf')
    pdf_report = open(filename, "wb")
    print('k')
    document = MyDocTemplate(pdf_report)
    templates = [MyTemplate(pdf_template_filename, name='background')]
    # pdf_template_filename2='chat.pdf'
    # templates = [MyTemplate(pdf_template_filename, name='background'),MyTemplate(pdf_template_filename2, name='background2') ]
    document.addPageTemplates(templates)

    styles = getSampleStyleSheet()
    elements = [NextPageTemplate('background')]
    elements.extend(create_toc())
    print('avt for')
    # Dummy content (hello world x 200)
    for i in range(2):
        page = PdfReader("chat.pdf").pages[0]
        # canvas.saveState()
        # rl_obj = makerl(canvas, self.page_template)
        # canvas.scale(self.page_xscale, self.page_yscale)
        # canvas.doForm(rl_obj)
        # canvas.restoreState()
        # elements.append(Paragraph(pagexobj(page), styles['Heading1']))
        elements.append(Paragraph("Hello World" + str(i), styles['Heading1']))
    print('apres for')
    document.multiBuild(elements)
    pdf_report.close()


if __name__ == '__main__':
    print('ici')
    try:
        print('ici2')
        output, template = sys.argv[1:]
        print('ici3')
        create_pdf(output, template)
    except ValueError:
        print("Usage: %s <output> <template>" % (sys.argv[0]))
