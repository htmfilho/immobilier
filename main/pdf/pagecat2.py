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

from reportlab.platypus import Paragraph, PageBreak

from reportlab.lib.styles import ParagraphStyle

from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate
from reportlab.platypus.frames import Frame


def pagecat2(request):
    doc = BaseDocTemplate('test.pdf')
    frame_title = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='title')
    frame_back = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='back')
    frame_1col = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col12')
    frame1_2col = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
    frame2_2col = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

    doc.addPageTemplates([
        PageTemplate(id='Title', frames=frame_title, onPage=static_title),
        PageTemplate(id='Back', frames=frame_back, onPage=static_back),
        PageTemplate(id='OneCol', frames=frame_1col, onPage=static_1col),
        PageTemplate(id='TwoCol', frames=[frame1_2col, frame2_2col], onPage=static_2col),
    ])
    story = [Paragraph('<b>Table of contents</b>', ParagraphStyle('normal')),
             NextPageTemplate('TwoCol'),
             PageBreak(),
             '<includePdfPages filename="pdf1.pdf" pages="1,2,3"/>',
             NextPageTemplate('TwoCol')]

    doc.build(story)
    return render(request, "test.html")


def static_title(canvas, doc):
    canvas.saveState()
    canvas.drawImage('logo-oditorium-whitebg.jpg', doc.width-2.5*inch, doc.height, width=4*inch, preserveAspectRatio=True)
    canvas.setFont('Times-Roman', 48)
    canvas.drawString(inch, doc.height - 1*inch, "TITLE")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Title - Page %d" % doc.page)
    canvas.restoreState()



def static_back(canvas, doc):
    canvas.saveState()
    canvas.drawImage('logo-oditorium-whitebg.jpg', doc.width-2.5*inch, doc.height, width=4*inch, preserveAspectRatio=True)
    canvas.setFont('Times-Roman', 48)
    canvas.drawString(inch, doc.height - 1*inch, "TITLE")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Title - Page %d" % doc.page)
    canvas.restoreState()


def static_1col(canvas, doc):
    canvas.saveState()
    canvas.drawImage('logo-oditorium-whitebg.jpg',
                     doc.width-2.5*inch, doc.height, width=4*inch,
                     preserveAspectRatio=True)
    canvas.setFont('Times-Roman', 48)
    canvas.drawString(inch, doc.height - 1*inch, "TITLE")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Title - Page %d" % doc.page)
    canvas.restoreState()


def static_2col(canvas, doc):
    canvas.saveState()
    canvas.drawImage('logo-oditorium-whitebg.jpg',
                     doc.width-2.5*inch, doc.height, width=4*inch,
                     preserveAspectRatio=True)
    canvas.setFont('Times-Roman', 48)
    canvas.drawString(inch, doc.height - 1*inch, "TITLE")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Title - Page %d" % doc.page)
    canvas.restoreState()
