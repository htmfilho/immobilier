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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import *
from main.forms.forms import FileForm

from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from django.utils.translation import ugettext_lazy as _
from reportlab.lib import utils

from reportlab.lib.pagesizes import A4 as A4

PAGE_SIZE = A4
MARGIN_SIZE = 15 * mm
COLS_WIDTH = [20*mm, 55*mm, 45*mm, 15*mm, 40*mm]
STUDENTS_PER_PAGE = 24
BOTTOM_MARGIN = 18
TOP_MARGIN = 85


def test_image(request):
    an_url = "http://media.rtl.fr/cache/7QbrYQMmo5-erboYCMOeZw/880v587-0/online/image/2016/0629/7783900500_chat-illustration.jpg"
    return build_pdf(an_url)


def build_pdf(image_file):
    filename = "%s.pdf" % _('scores_sheet')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=PAGE_SIZE,
                            rightMargin=MARGIN_SIZE,
                            leftMargin=MARGIN_SIZE,
                            topMargin=TOP_MARGIN,
                            bottomMargin=BOTTOM_MARGIN)
    image1 = get_image2(image_file)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    content = [image1]
    p = ParagraphStyle('legend')
    p.textColor = 'grey'
    p.borderColor = 'grey'
    p.borderWidth = 1
    p.alignment = TA_CENTER
    p.fontSize = 8
    p.borderPadding = 5

    legend_text = 'justification_legend'
    legend_text += "<br/><font color=red>%s</font>" % 'fffff'

    content.append(Paragraph('''
                            <para>
                                %s
                            </para>
                            ''' % legend_text, p))
    doc.build(content)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def upload(request):
    list_extension_image = ['jpg', 'jpge', 'png', 'gif']
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            if file_name is not None:
                if 'image' in file_name.content_type:
                    return build_pdf(file_name)

        return HttpResponseRedirect(reverse('test'))


def get_image(path, width, doc):
    max_widh = doc.width - (MARGIN_SIZE*2)-50
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    pw, ph = A4
    height = ih

    if iw > max_widh:
        width = max_widh
        ratio = width/max_widh
        height = ih/ratio

    return Image(path, width=width, height=height)


def get_image2(path):
    img = utils.ImageReader(path)
    xsize, ysize = img.getSize()

    width, height = A4
    width = width - (MARGIN_SIZE * 2)
    height = height - (BOTTOM_MARGIN + TOP_MARGIN)
    Im = Image(path)

    if xsize > ysize:  #deal with cases were xsize is bigger than ysize
        if xsize > width:
            nxsize = width - 12
            nysize = int(ysize*(nxsize/xsize))  #make ysize
            xsize = nxsize
            ysize = nysize

            return Image(path, width=nxsize, height=nysize)
    else:  #deal with cases where ysize is bigger than xsize
        if ysize > height:
            nysize = height - 12
            a = nysize/ysize
            nxsize = xsize * a
            xsize = int(nxsize)
            ysize = int(nysize)

            return Image(path, width=nxsize, height=nysize)
    return Image(path)
