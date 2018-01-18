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
from django.views.generic import *

from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import Paragraph

from reportlab.lib.styles import ParagraphStyle
from django.utils.translation import ugettext_lazy as _
from PyPDF2 import PdfFileReader

from reportlab.platypus.tableofcontents import TableOfContents




class MyDocTemplate(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'normal':
                self.notify('TOCEntry', (0, text, self.page))


def essai(request):
    filename = "%s.pdf" % _('scores_sheet')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]

    buffer = BytesIO()

    doc = MyDocTemplate(buffer,
                        pagesize=PAGE_SIZE,
                        rightMargin=MARGIN_SIZE,
                        leftMargin=MARGIN_SIZE,
                        topMargin=85,
                        bottomMargin=18)
    content = []

    # to
    # fin toc
    # merge
    if not pdfs or len(pdfs) < 2:
        exit("Please enter at least two pdfs for merging!")
    no_page = 1
    manual_toc = True
    if manual_toc:
        toc = TableOfContents()

        cpt = 0

        for fname in pdfs:
            input = PdfFileReader(open(fname, 'rb'))
            number_of_page = input.getNumPages()

            content.append(Paragraph('''
                                    <para>
                                        %s       %s-%s %s
                                    </para>
                                    ''' % (fname, no_page, no_page + number_of_page, lien), ParagraphStyle('normal')))
            # content.append(lien)
            no_page = no_page + number_of_page
            cpt = cpt + 1

        content.append(toc)
    doc.multiBuild(content)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

