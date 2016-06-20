from django.shortcuts import render
from PyPDF2.pdf import RectangleObject
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen.canvas import Canvas
from main.models import *
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
import os
from .exportUtils import export_xls_batiment
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
from django.db import models
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy
from main.forms import PersonneForm, BatimentForm, ProprietaireForm, FraisMaintenanceForm, SocieteForm, ContratLocationForm, FileForm
import datetime

from dateutil.relativedelta import relativedelta
from . import batiment, proprietaire, suivis, alertes, contratlocation, financement, locataire, contratgestion
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether, KeepInFrame, BaseDocTemplate

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from django.utils.translation import ugettext_lazy as _
import datetime
import json
import sys
import PyPDF2
from PyPDF2 import PdfFileMerger,  PdfFileReader, PdfFileWriter
from io import StringIO
from urllib.request import urlopen
from urllib.request import Request
from django.conf import settings
import os
from  reportlab.platypus.tableofcontents import TableOfContents
import os.path
from reportlab.lib import utils

from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import A4 as A4
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame

PAGE_SIZE = A4
MARGIN_SIZE = 15 * mm
COLS_WIDTH = [20*mm,55*mm,45*mm,15*mm,40*mm]
STUDENTS_PER_PAGE = 24
BOTTOM_MARGIN = 18
TOP_MARGIN = 85

class MyDocTemplateMerge(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)


    def afterFlowable(self, flowable):
         print('afterFlowable')
         "Registers TOC entries."
         if flowable.__class__.__name__ == 'Paragraph':
             text = flowable.getPlainText()
             print('kkkkk',flowable)
             style = flowable.style.name
             print('style',style)
             if style == 'normal':
                 self.notify('TOCEntry', (0, text, self.page))

def merge_pdf():
    print('merge_pdf')
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs=[pdf1,pdf2, ]
    #
    buffer = BytesIO()

    doc = MyDocTemplateMerge(buffer,
                            pagesize=PAGE_SIZE,
                            rightMargin=MARGIN_SIZE,
                            leftMargin=MARGIN_SIZE,
                            topMargin=85,
                            bottomMargin=18)

    content = []


    # merge


    if not pdfs or len(pdfs) < 2:
        exit("Please enter at least two pdfs for merging!")
    no_page=2
    manual_toc = True
    if manual_toc:
        print('manual_toc')
        cpt = 0
        content.append(Paragraph('Table of contents' , ParagraphStyle('normal')))
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

            content.append(Paragraph('%s          %s-%s' % (fname, no_page, no_page + number_of_page), ParagraphStyle('normal')))
            # ancre = '<a name="%s"></a>' % fname
            # content.append(Paragraph('''
            #                             %s
            #                         ''' % (ancre), ParagraphStyle('normal')))
            no_page = no_page + number_of_page
            cpt = cpt +1



    doc.build(content)#ne garnit que la 1iere page
    #doc.build(content, canvasmaker=NumberedCanvas)
    merger = PdfFileMerger()


    merger.setPageMode('/UseOC')
    merger.append(buffer)
    num_page = 1
    no_page=1
    cpt=0
    for fname in pdfs:
        print('for')
        input = PdfFileReader(open(fname, 'rb'))

        number_of_page = input.getNumPages()
        lien = "lnk2_" + str(no_page)
        lien=fname
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


        num_page=num_page+1
        no_page = no_page + number_of_page
        cpt=cpt+1


    output = open("output.pdf", "wb")
    merger.write(output)
    output.close()


if __name__ == '__main__':

    merge_pdf()