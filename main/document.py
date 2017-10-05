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
from main.pages_utils import PAGE_LISTE_BATIMENTS
import re
import pdfkit


def document_bd_list(request):
    return render(request, "documents/document_list.html",
                  {'documents': mdl.modele_document.find_all()})


def document_form(request, document_id):
    return render(request, "documents/document_form.html",
                  {'document': mdl.modele_document.find_by_id(document_id)})


def lettre_indexation_form(request, contrat_location_id):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    form = None
    formset = None
    contrat_location = None
    if request.method == 'POST':
        pass
    else:
        if contrat_location_id:
            contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)

        ArticleFormSet = formset_factory(LigneForm, extra=2)
        formset = None
        # formset = ArticleFormSet(initial=[{'test': 'Django is now open source', },
        #                                   {'test': 'Django is now open source2', }])
        #
        form = LettreForm(initial={'sujet': modele.sujet,
                                   'format': "docx",
                                   'fichier_modele': modele.fichier_modele,
                                   'titre': 'Monsieur',
                                   'tableSet': formset})
    # form = LettreForm(request.POST or None)
    return render(request, "documents/lettre.html", {'form': form,
                                                     'formset': formset,
                                                     'contrat_location': contrat_location,
                                                     'modele':  modele})


def lettre_indexation(request, contrat_location_id):
    modele = mdl.modele_document.find_by_reference('LETTRE_INDEXATION')
    a_contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)

    doctype = request.POST.get('format_fichier', 'pdf')

    data = {}
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

    data.update({'dateJour':  timezone.now()})
    locataires = a_contrat_location.locataires
    locataire = locataires.first()
    if locataire:
        personne = locataire.personne
        if locataire.civilite:
            data.update({'titre': locataire.civilite.capitalize()})
        else:
            data.update({'titre': 'Madame, Monsieur,'})
    else:
        personne = None

    data.update({"sujet": "Lettre d'indexation"})
    if personne:
        data.update({'nom': personne.nom})
        data.update({'prenom': personne.prenom})

    bat = a_contrat_location.batiment
    if bat:
        data.update({'adresse': bat.adresse_rue})
        data.update({'localite': bat.adresse_localite})
    personne_gestionnaire = mdl.personne.find_gestionnaire_default()
    data.update({'gestionnaire_nom': personne_gestionnaire.nom})
    data.update({'gestionnaire_prenom': personne_gestionnaire.prenom})

    filename = fill_template(
        "documents/{}".format(modele.fichier_modele), data,
        output_format=doctype)
    visible_filename = 'LETTRE_INDEXATION.{}'.format(doctype)

    return FileResponse(filename, visible_filename)


class LigneTest:

    def __init__(self):
        self.col1 = "Ferrari"
        self.col2 = "Ferrari"

    def ligne_complete(self):
        return "{0} {1}".format(self.col1, self.col2)


def lettre_indexation_new(request, contrat_location_id):
    document_modele = mdl.document_modele.find_by_reference('LETTRE_INDEXATION')
    if document_modele:
        variables = {}
        input = document_modele.contenu
        ll = re.findall(r"\[([^\]]*)\]*", input)
        un_contrat_location = mdl.contrat_location.find_by_id(contrat_location_id)
        if un_contrat_location:
            if un_contrat_location.batiment:
                batiment = un_contrat_location.batiment
                variables.update({'batiment_description': batiment.description,
                                  'batiment_rue': batiment.rue,
                                  'batiment_numero': batiment.numero,
                                  'batiment_boite': batiment.boite,
                                  'batiment_lieu_dit': batiment.lieu_dit,
                                  'batiment_localite': batiment.localite,
                                  'batiment_superficie': batiment.superficie,
                                  'batiment_performance_energetique': batiment.performance_energetique})


        for key in ll:
            value = ''
            if key not in variables:
                variables.update({'{}'.format(key): value})
            else:
                input = input.replace(key, 'kkk')

        return render(request, 'documents/document.html', {'document': document_modele,
                                                           'contenu': input,
                                                           'variables': variables})
