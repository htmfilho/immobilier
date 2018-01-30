##############################################################################
#
#    Immobilier it's an application
#    designed to manage the core business of property management, buildings,
#    rental agreement and so on.
#
#    Copyright (C) 2016-2018 Verpoorten Leïla
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.l
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
from django.db import models
from ckeditor.fields import RichTextField


class DocumentModele(models.Model):
    # TYPE_DOCUMENT = (
    # ('LETTRE_INDEXATION', 'Lettre indexation'),
    # )
    reference = models.CharField(max_length=50, blank=True, null=True)
    contenu = RichTextField()
    sujet = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.reference


def find_by_reference(a_reference):
    return DocumentModele.objects.get(reference=a_reference)


def find_all():
    return DocumentModele.objects.all()


def find_by_id(a_document_id):
    return DocumentModele.objects.get(pk=a_document_id)