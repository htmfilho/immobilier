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
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from main import models as mdl
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy
from main.forms import BatimentForm, ProprietaireForm, FraisMaintenanceForm, SocieteForm, FileForm, LettreForm, \
    LigneForm

from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from django.utils.translation import ugettext_lazy as _
from PyPDF2 import PdfFileMerger,  PdfFileReader, PdfFileWriter
from django.conf import settings
from reportlab.lib import utils

from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import A4 as A4
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, NextPageTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
import datetime

from templated_docs import fill_template
from templated_docs.http import FileResponse
from django.forms import formset_factory


class ContratGestionList(ListView):
    model = mdl.contrat_gestion


class ContratGestionDetail(DetailView):
    model = mdl.contrat_gestion


class FraisMaintenanceList(ListView):
    model = mdl.frais_maintenance


class FraisMaintenanceDetail(DetailView):
    model = mdl.frais_maintenance


def merge_pdf4(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]
    #
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
    no_page = 0
    width, height = A4

    output.addBlankPage(width, height)
    cur = 1
    cur_prev = 0
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))

        number_of_page = input.getNumPages()
        output.addPage(input.getPage(0))

        # if no_page ==0:
        #     parent = output.addBookmark("One", no_page, None)
        # else:
        #     output.addBookmark("One", no_page, parent)
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


def dashboard(request):
    return render(request, 'main/dashboard.html', {})


def home(request):
    suivis = mdl.suivi_loyer.find_suivis_a_verifier_proche()
    suivis_recus = mdl.suivi_loyer.find_suivis_by_etat_suivi(timezone.now(), 'PAYE')
    suivis_recus = mdl.suivi_loyer.find_mes_suivis_by_etat_suivi(timezone.now(), 'PAYE')
    suivis_non_paye = mdl.suivi_loyer.find_suivis_by_pas_etat_suivi(timezone.now(), 'PAYE')
    montant_recu = 0
    montant_attendu = 0
    mois_en_cours = str(datetime.datetime.now().month) + "/" + str(datetime.datetime.now().year)
    mes_frais = mdl.frais_maintenance.find_mes_frais_du_mois()

    return render(request, 'myhome.html',
                  {'alertes':         mdl.alerte.find_by_etat('A_VERIFIER'),
                   'batiments':       mdl.batiment.find_batiments_gestionnaire(),
                   'contrats':        mdl.contrat_gestion.find_my_contrats(),
                   'honoraires':      mdl.honoraire.find_honoraires_by_etat_today('A_VERIFIER'),
                   'suivis':          suivis,
                   'previous':        request.POST.get('previous', None),
                   'suivis_recus':    suivis_recus,
                   'montant_recu':    montant_recu,
                   'montant_attendu': montant_attendu,
                   'suivis_non_paye': suivis_non_paye,
                   'locataires':      mdl.locataire.find_my_locataires(),
                   'mois_en_cours':   mois_en_cours,
                   'mes_frais':       mes_frais,
                   'tot_depenses':    get_total_depenses(mes_frais),
                   'tot_recettes':    get_total_recettes(suivis_recus)})


def get_total_depenses(mes_frais):
    tot_depenses = 0
    for f in mes_frais:
        if f.montant:
            tot_depenses += f.montant
    return tot_depenses


def get_total_recettes(suivis_recus):
    tot_recettes = 0
    if suivis_recus:
        for s in suivis_recus:
            if s.loyer_percu:
                tot_recettes = tot_recettes + s.loyer_percu
            if s.charges_percu:
                tot_recettes = tot_recettes + s.charges_percu
    return tot_recettes


def listeBatiments(request):
    batiments = mdl.batiment.find_all()
    return render(request, 'batiment/listeBatiments.html',
                  {'batiments': batiments,
                   'proprietaires': mdl.proprietaire.find_distinct_proprietaires()})

@login_required
def listeComplete(request):
    batiments = mdl.batiment.find_all()
    contrats_location = mdl.contrat_location.find_all()
    return render(request, 'listeComplete.html', {'batiments': batiments})


@login_required
def personne(request, personne_id):
    personne = mdl.personne.find_personne(personne_id)
    return render(request, "personne/personne_form.html",
                  {'personne': personne,
                   'societes': mdl.societe.find_all()})


def update_personne(request):
    personne = mdl.personne.Personne()
    print(request.POST.get('action', None))
    if 'add' == request.POST.get('action', None) or 'modify' == request.POST.get('action', None):
        print(request.POST['id'])
        personne = get_object_or_404(mdl.personne.Personne, pk=request.POST['id'])
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']

        personne.save()
    return render(request, "personne/personne_form.html",
                  {'personne': personne,
                   'societes': mdl.societe.find_all()})


def xlsRead(request):
    short_description = u"Export XLS"


class FraisMaintenanceCreate(CreateView):
    model = mdl.frais_maintenance
    form_class = FraisMaintenanceForm


class FraisMaintenanceUpdate(UpdateView):
    model = mdl.frais_maintenance
    form_class = FraisMaintenanceForm


class FraisMaintenanceDelete(DeleteView):
    model = mdl.frais_maintenance
    success_url = reverse_lazy('fraismaintenance-list'),


class PersonneDelete(DeleteView):
    model = mdl.personne
    success_url = "../../../personnes"


class BatimentList(ListView):
    model = mdl.batiment


class BatimentCreate(CreateView):
    model = mdl.batiment
    form_class = BatimentForm


class BatimentUpdate(UpdateView):
    model = mdl.batiment
    form_class = BatimentForm


class BatimentDelete(DeleteView):
    model = mdl.batiment
    success_url = "../../../batiments"


class ProprietaireList(ListView):
    model = mdl.proprietaire


class ProprietaireDetail(DetailView):
    model = mdl.proprietaire


class ProprietaireCreate(CreateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm

    def form_valid(self, form):
        print('form valid')
        proprietaire = form.save(commit=False)
        # article.author = self.request.user
        return super(ProprietaireCreate, self).form_valid(form)


class ProprietaireCreateForBatiment(CreateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm

    def get_initial(self):
        initial_data = super(ProprietaireCreateForBatiment, self).get_initial()
        course = get_object_or_404(mdl.batiment.Batiment, pk=self.kwargs['pk'])
        if course:
            initial_data['batiment'] = course
        # if self.form_class == TransferFormFrom:
        #     initial_data['from_account'] = self.acct_pk
        # elif self.form_class == TransferFormTo:
        #     initial_data['to_account'] = self.acct_pk
        # else:
        #     raise ImproperlyConfigured(
        #                 '"form_class" variable must be defined '
        #                 'in %s for correct initial behavior.'
        #                 % (self.__class__.__name__,
        #                    obj.__class__.__name__))
        return initial_data
    # def get_form(self, form_class):
    #     form = super(ProprietaireCreateForBatiment, self).get_form(form_class)
    #     course = get_object_or_404(mdl.batiment.Batiment, pk=self.kwargs['pk'])
    #
    #     form.instance.batiment = course
    #     print (course)
    #     # return form
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)
    # def form_valid(self, form):
    #     print('kkk')
    #     print(self.kwargs['pk'])
    #     form.instance.batiment = get_object_or_404(Event,
    #                                             pk=self.kwargs['pk'])
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)
    # def get_form_class(self):
    #     return ProprietaireForm
    #
    # def get_form_kwargs(self, **kwargs):
    #     print('get_form_kwargs')
    #     kwargs = super(ProprietaireCreateForBatiment, self).get_form_kwargs(**kwargs)
    #     print (kwargs)
    #     if 'pk' in kwargs:
    #         print(self.kwargs['pk'])
    #         batiment = mdl.batiment.objects.get(pk=self.kwargs['pk'])
    #         instance = Proprietaire(batiment=batiment)
    #         kwargs.update({'instance': instance})
    #     else:
    #         print('les')
    #     return
    #

    def form_valid(self, form):
        proprietaire = form.save(commit=False)
        # article.author = self.request.user
        return super(ProprietaireCreateForBatiment, self).form_valid(form)
    #
    # def dispatch(self, request, *args, **kwargs):
    #     print('displath')
    #     self.batiment = mdl.batiment.objects.get(pk=self.kwargs['pk'])
    #     print (self.batiment)
    #
    #     return super(ProprietaireCreateForBatiment, self).dispatch(request, *args, **kwargs)

    #
    # def form_valid(self, form):
    #     print('form_valid')
    #     form.instance.batiment= self.batiment
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)

    #
    # form_class = ProprietaireForm
    # batiment = mdl.batiment.objects.get(pk=1)
    # form_class.batiment = batiment
    # # fields = ['batiment']
    #
    # def form_valid(self, form):
    #     print('form_valid')
    #     form.instance.batiment = mdl.batiment.objects.get(pk=self.kwargs['class'])
    #     # event = Event.objects.get(pk=self.kwargs['class'])
    #     return super(ProprietaireCreateForBatiment, self).form_valid(form)


class ProprietaireUpdate(UpdateView):
    model = mdl.proprietaire
    form_class = ProprietaireForm


class ProprietaireDelete(DeleteView):
    model = mdl.proprietaire
    success_url = "../../../proprietaires"


class SocieteList(ListView):
    model = mdl.societe


class SocieteDetail(DetailView):
    model = mdl.societe


class SocieteCreate(CreateView):
    model = mdl.societe
    form_class = SocieteForm


class SocieteUpdate(UpdateView):
    model = mdl.societe
    form_class = SocieteForm


class SocieteDelete(DeleteView):
    model = mdl.societe
    success_url = "../../../societes"


class HonoraireDelete(DeleteView):
    model = mdl.honoraire
    success_url = "../../../honoraires"

PAGE_SIZE = A4
MARGIN_SIZE = 15 * mm
COLS_WIDTH = [20*mm, 55*mm, 45*mm, 15*mm, 40*mm]
STUDENTS_PER_PAGE = 24
BOTTOM_MARGIN = 18
TOP_MARGIN = 85


def test_merge(request):
    return merge_pdf(request)
    # return merge_pdf2(request)
    # return merge_pdf4(request)
    # return essai(request)
    # return pagecat(request)
    # return pagecat2(request)


def test(request):
    return render(request, "test.html")


def test_image(request):
    return build_pdf("http://www.louisetzeliemartin.org/medias/images/chat-1.jpg")
    # return render(request, "test.html")


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


def merge_pdf(request):
    print('merge_pdf')
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
        print('manual_toc')
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
        print('for')
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


def upload(request):
    list_extension_image = ['jpg', 'jpge', 'png', 'gif']
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.FILES['file']
            if file_name is not None:
                print(file_name.content_type)
                if 'image' in file_name.content_type:
                    print('image')
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


def merge_pdf2(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]
    #
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer,
                            pagesize=PAGE_SIZE,
                            rightMargin=MARGIN_SIZE,
                            leftMargin=MARGIN_SIZE,
                            topMargin=85,
                            bottomMargin=18)

    content = []

    # to
    # fin toc
    # merge
    print('merge_pdf')

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
    # output.addPage(buffer)
    num_page = 0
    no_page = 0
    width, height = A4

    output.addBlankPage(width, height)
    cur = 1
    cur_prev = 0
    for fname in pdfs:
        input = PdfFileReader(open(fname, 'rb'))

        number_of_page = input.getNumPages()
        output.addPage(input.getPage(0))

        # if no_page ==0:
        #     parent = output.addBookmark("One", no_page, None)
        # else:
        #     output.addBookmark("One", no_page, parent)
        output.addBookmark(str(no_page), num_page)
        num_page = num_page+1
        no_page = no_page + 1

        rect = RectangleObject([400, 400, 600, 600])
        output.addLink(cur_prev, cur, rect)
        cur_prev = cur_prev + 1
        cur = cur + 1
    d = open("output.pdf", "wb")

    # merger.write(output)
    # merger.write(doc)
    output.write(d)
    d.close()
    return render(request, "test.html")


def add_header_footer(canvas, doc):
    canvas.saveState()
    print('add_header_footer')
    canvas.restoreState()


def makeTocHeaderStyle(level,  fontName='Times-Roman'):
    assert level >= 0, "Level must be >= 0."

    PS = ParagraphStyle
    size = 12
    style = PS(name='Heading' + str(level),
               fontName=fontName,
               fontSize=size,
               leading=size*1.2,
               spaceBefore=size/4.0,
               spaceAfter=size/8.0)

    return style


def essai(request):
    filename = "%s.pdf" % _('scores_sheet')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs = [pdf1, pdf2]
    #
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
        print('manual_toc')
        toc = TableOfContents()

        cpt = 0

        for fname in pdfs:
            input = PdfFileReader(open(fname, 'rb'))
            number_of_page = input.getNumPages()
            if cpt > 0:
                lien = '<link href="http://uclouvain.be/index.html" color="blue">is a link to</link>'
            else:
                lien = '<link href="#lnk_1" color="blue">is a link to</link>'
            lien = "kk"
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


class MyDocTemplateMerge(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterFlowable(self, flowable):
         print('afterFlowable')
         "Registers TOC entries."
         if flowable.__class__.__name__ == 'Paragraph':
             text = flowable.getPlainText()
             style = flowable.style.name
             print('style', style)
             if style == 'normal':
                 self.notify('TOCEntry', (0, text, self.page))


class MyDocTemplate(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterFlowable(self, flowable):
         """Registers TOC entries."""
         if flowable.__class__.__name__ == 'Paragraph':
             text = flowable.getPlainText()
             style = flowable.style.name
             print('style', style)
             if style == 'normal':
                 self.notify('TOCEntry', (0, text, self.page))


def merge_pdf3(request):
    pdf1 = "pdf1.pdf"
    pdf2 = "pdf2.pdf"

    pdfs=[pdf1, pdf2]
    #
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer,
                            pagesize=PAGE_SIZE,
                            rightMargin=MARGIN_SIZE,
                            leftMargin=MARGIN_SIZE,
                            topMargin=85,
                            bottomMargin=18)

    content = []
    print('merge_pdf')

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
    no_page=1
    cpt=0

    for fname in pdfs:
        print('for')
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


class DocTemplateWithTOC(SimpleDocTemplate):

    def __init__(self, indexedFlowable, filename, firstPageNumber=1, **kw):
        """toc is the TableOfContents object
        indexedFlowale is a dictionnary with flowables as key and a dictionnary as value.
            the sub-dictionnary have two key:
                text: the text which will br print in the table
                level: the level of the entry( modifying the indentation and the police
        """
        self._toc = []
        self._tocStory = []
        self._indexedFlowable = indexedFlowable
        self._filename = filename
        self._part = ""
        self._firstPageNumber = firstPageNumber
        SimpleDocTemplate.__init__(self, filename, **kw)

        self._PAGE_HEIGHT = self.pagesize[1]
        self._PAGE_WIDTH = self.pagesize[0]

    def afterFlowable(self, flowable):
        if flowable in self._indexedFlowable:
            self._toc.append((self._indexedFlowable[flowable]["level"], self._indexedFlowable[flowable]["text"], self.page + self._firstPageNumber - 1))
        try:
            if flowable.getPart() != "":
                self._part = flowable.getPart()
        except:
            pass

    def handle_documentBegin(self):
        self._part = ""
        SimpleDocTemplate.handle_documentBegin(self)

    def _prepareTOC(self):
        headerStyle = ParagraphStyle({})
        headerStyle.fontName = "LinuxLibertine-Bold"
        headerStyle.alignment = TA_CENTER
        entryStyle = ParagraphStyle({})
        entryStyle.fontName = "LinuxLibertine"
        entryStyle.spaceBefore = 8
        self._tocStory.append(PageBreak())
        self._tocStory.append(Spacer(cm, 1*cm))
        self._tocStory.append(Paragraph(_("Table of contents"), headerStyle))
        self._tocStory.append(Spacer(cm, 2*cm))


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


# Entries to the table of contents can be done either manually by
# calling the addEntry method on the TableOfContents object or automatically
# by sending a 'TOCEntry' notification in the afterFlowable method of
# the DocTemplate you are using. The data to be passed to notify is a list
# of three or four items countaining a level number, the entry text, the page
# number and an optional destination key which the entry should point to.
# This list will usually be created in a document template's method like
# afterFlowable(), making notification calls using the notify() method
# with appropriate data.

     def afterFlowable(self, flowable):
         """Registers TOC entries."""
         if flowable.__class__.__name__ == 'Paragraph':
             text = flowable.getPlainText()
             style = flowable.style.name
             if style == 'Heading1':
                 self.notify('TOCEntry', (0, text, self.page))
             if style == 'Heading2':
                 self.notify('TOCEntry', (1, text, self.page))


def pagecat(request):
    print('pagecat')
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
        ParagraphStyle(fontName='Times-Bold', fontSize=20, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=10, leading=16),
        ParagraphStyle(fontSize=18, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5, leading=12),
    ]
    Story.append(toc)
    manual_toc = True
    if manual_toc:
        print('manual_toc')
        cpt = 0
        Story.append(Paragraph('<b>Table of contents</b>', centered))
        for fname in pdfs:
            Story.append(Paragraph('<includePdfPages filename="%s" pages="1" outlineText="crasher"/>' % fname, h1))

            Story.append(Paragraph('%s' % fname, h2))
            cpt = cpt + 1
    doc = MyDocTemplate('mintoc.pdf')

    doc.multiBuild(Story)
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


def add_header_footer(canvas, doc):
    print('add_header_footer')
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


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
                             "Page %d of %d" % (self._pageNumber, page_count))


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


def personne_delete(request, id):
    mdl.personne.delete_personne(int(id))
    return HttpResponseRedirect(reverse('personne_search'))


def lettre_form(request):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    form = None
    formset = None
    if request.method == 'POST':
        pass
    else:
        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                          {'test': 'Django is now open source2', }])

        form = LettreForm(initial={'sujet': modele.sujet, 'format': "docx", 'fichier_modele': modele.fichier_modele,
                                   'titre': 'Monsieur',
                                   'tableSet': formset})
    # form = LettreForm(request.POST or None)
    return render(request, "lettre.html", {'form': form, 'formset': formset})


def lettre_create(request):
    print('lettre_view')
    formset = None
    if request.method == 'POST':
        form = LettreForm(request.POST or None)
        print(form)
        formset = LigneForm(request.POST or None)
        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                          {'test': 'Django is now open source2', }])
    else:
        form = LettreForm()

    print(form.errors)
    if formset.is_valid():
        print('formset valid')
    else:
        print('formset invalid')
    if form.is_valid():
        print('form valid')

        doctype = form.cleaned_data['format']
        data = form.cleaned_data
        lignes = []
        ligne1 = LigneTest()
        ligne1.col1 = "col1"
        ligne1.col2 = "col2"

        ligne2 = LigneTest()
        ligne2.col1 = "col12"
        ligne2.col2 = "col22"

        lignes.append(ligne1)
        lignes.append(ligne2)
        #  lignes = [["ii","oo"],["ii2","oo2"]]
        data.update({'lignes': lignes})
        data.update({'l1': 'l1'})
        data.update({'l2': 'l2'})
        data.update({'html': '<table><tr><td>sss</td><td>ksdf</td></tr></table>'})

        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
                                          {'test': 'Django is now open source2', }])
        data.update({'formset': formset})

        data.update({'dateJour': timezone.now()})
        personne = mdl.personne.find_personne(1)
        data.update({'nom': personne.nom})
        data.update({'prenom': personne.prenom})
        bat = mdl.batiment.find_batiment(1)
        data.update({'adresse': bat.adresse_rue})
        data.update({'localite': bat.adresse_localite})
        personne_gestionnaire = mdl.personne.find_gestionnaire_default()
        data.update({'gestionnaire_nom': personne_gestionnaire.nom})
        data.update({'gestionnaire_prenom': personne_gestionnaire.prenom})

        filename = fill_template(
            'documents/lettre.odt', data,
            output_format=doctype)
        visible_filename = 'invoice.{}'.format(doctype)

        return FileResponse(filename, visible_filename)
    else:
        print('form invalid')
        print(form.errors)
        return render(request, 'documents/lettre.html', {'form': form, 'formset': formset})


class LigneTest:

    def __init__(self):
        self.col1 = "Ferrari"
        self.col2 = "Ferrari"

    def ligne_complete(self):
        return "{0} {1}".format(self.col1, self.col2)

